import pandas as pd

# Define the columns for each band
delta_cols = ['Delta_TP9', 'Delta_AF7', 'Delta_AF8', 'Delta_TP10']
theta_cols = ['Theta_TP9', 'Theta_AF7', 'Theta_AF8', 'Theta_TP10']
alpha_cols = ['Alpha_TP9', 'Alpha_AF7', 'Alpha_AF8', 'Alpha_TP10']
beta_cols = ['Beta_TP9', 'Beta_AF7', 'Beta_AF8', 'Beta_TP10']
gamma_cols = ['Gamma_TP9', 'Gamma_AF7', 'Gamma_AF8', 'Gamma_TP10']

# List of all band columns
cols = delta_cols + theta_cols + alpha_cols + beta_cols + gamma_cols


def clean_and_transform_data(df):
    """
    Cleans the DataFrame by dropping nulls, selecting necessary columns, and transforming EEG power values.
    """
    df = df.drop(columns=['Elements'])
    # Drop rows with any null values
    df = df.dropna()

    # Select necessary columns
    necessary_columns = ['TimeStamp', 'Heart_Rate'] + cols
    df = df[necessary_columns]

    

    # Apply log relative power transformation
    add_log_relative_power_columns(df, cols)

    # Add average, frontal, and posterior columns for each frequency band
    add_band_average_columns(df)

    # Add creativity metrics
    add_creativity_metrics(df)

    # Add relaxation metrics
    add_relaxation_metrics(df)
    add_relaxation_metrics_2(df)

    # Add regeneration metrics
    add_regeneration_metrics(df)

    # Add engagement metrics
    add_engagement_metrics(df)
    add_engagement_metrics_v2(df)

    # Calculate and add the HRV column
    add_hrv_column(df)

    # Resample the data to 1-minute intervals
    df = resample_data(df)

    # Add the Sleep/Awake column
    add_sleep_awake_column(df)

    # Add the dummy column
    add_dummy_column(df)
    # Drop the unnecessary columns
    df.drop(cols, axis=1, inplace=True)

    # Drop first 3 and last 3 rows
    df = df.iloc[3:-3]
    
    return df

def resample_data(df):
    """
    Resamples the DataFrame to 1-minute intervals, aggregating values by their mean in each interval.
    Resets the index to turn 'TimeStamp' back into a column.
    """

    df.set_index('TimeStamp', inplace=True)
    # Resample the data to 1-minute intervals, taking the mean of each interval
    df_resampled = df.resample('1T').mean()
    
    # Reset the index to make 'TimeStamp' a column again
    df_resampled.reset_index(inplace=True)
    
    return df_resampled


def add_dummy_column(df):
    """
    Adds a dummy column with all values set to 'dummy'.
    """
    df['dummy'] = 'frequency bands'


def add_hrv_column(df):
    """
    Adds a Heart Rate Variability (HRV) column to the DataFrame based on the Heart_Rate column.
    """
    df['HRV'] = 60 / df['Heart_Rate'] * 100

def add_sleep_awake_column(df):
    """
    Adds a Sleep/Awake column to the DataFrame based on the HRV column.
    """
    df['Sleepy'] = (df['Delta_AVG'] + df['Theta_AVG'] ) / 2
    df['Awake'] = (df['Beta_AVG'] + df['Alpha_AVG'] ) / 2


def add_band_average_columns(df):
    """
    Adds average, frontal, and posterior columns for each frequency band.
    """
    # Define the frequency bands and their corresponding columns
    bands = {
        'Delta': delta_cols,
        'Theta': theta_cols,
        'Alpha': alpha_cols,
        'Beta': beta_cols,
        'Gamma': gamma_cols
    }

    for band_name, band_cols in bands.items():
        # Calculate and add the average column for the current band
        
        df[f'{band_name}_AVG'] = df[band_cols].mean(axis=1)
        #format 7 decimal places
        #df[f'{band_name}_AVG_rel'] = df[f'{band_name}_AVG_rel'].map(lambda x: format(x, '.3f'))
        
        # Frontal columns are those ending with 'AF7' and 'AF8'
        frontal_cols = [col for col in band_cols if col.endswith('AF7') or col.endswith('AF8')]
        df[f'{band_name}_Frontal'] = df[frontal_cols].mean(axis=1)
        #format 7 decimal places
        #df[f'{band_name}_Frontal_rel'] = df[f'{band_name}_Frontal_rel'].map(lambda x: format(x, '.3f'))
        
        # Posterior columns are those ending with 'TP9' and 'TP10'
        posterior_cols = [col for col in band_cols if col.endswith('TP9') or col.endswith('TP10')]
        df[f'{band_name}_Posterior'] = df[posterior_cols].mean(axis=1)
        #format 7 decimal places
        #df[f'{band_name}_Posterior_rel'] = df[f'{band_name}_Posterior_rel'].map(lambda x: format(x, '.3f'))

    #delete cols_rel  BURASI SONRASI ICIN SILMEK GEREKEBILIR
    # df.drop(cols, axis=1, inplace=True)
   
        
def add_log_relative_power_columns(df, band_cols):
    """
    Converts EEG power values from decibels to relative power values.
    """
    for sensor_suffix in ['TP9', 'AF7', 'AF8', 'TP10']:
        # Extract columns for the current sensor
        sensor_cols = [col for col in band_cols if col.endswith(sensor_suffix)]
        # Calculate 10^absolute power for each band
        pow_10_abs = df[sensor_cols].apply(lambda x: 10**x)
        # Calculate the sum of 10^absolute powers for all bands for the current sensor
        sum_pow_10_abs = pow_10_abs.sum(axis=1)
        # Calculate and add relative power columns
        for col in sensor_cols:
            relative_col_name = f'{col}'
            df[relative_col_name] = (10**df[col]) / sum_pow_10_abs
            # format 7 decimal places
            #df[relative_col_name] = df[relative_col_name].apply(lambda x: round(x, 7))



def add_creativity_metrics(df):
    """
    Adds creativity metrics by first converting theta and beta power values from dB to a linear scale
    for the purpose of these calculations, then dividing theta power columns by beta columns for each sensor,
    and calculates average, frontal, and posterior creativity metrics.
    """
    # Initialize a temporary DataFrame for creativity calculations
    creativity_df = pd.DataFrame()

    # Convert Theta and Beta power values from dB to linear scale and calculate Theta/Beta for each sensor
    for theta_col, beta_col in zip(theta_cols, beta_cols):
        # theta_linear = 10 ** (df[theta_col] )
        # beta_linear = 10 ** (df[beta_col] )
        creativity_col = f'Creativity_{theta_col.split("_")[1]}'
        creativity_df[creativity_col] = df[theta_col] / df[beta_col]

    # Calculate Creativity_AVG and add it to the original DataFrame
    df['Creativity_AVG'] = creativity_df.mean(axis=1)

    # Calculate Creativity_Frontal, normalize to show as percentage, and add it to the original DataFrame
    creativity_frontal_cols = [col for col in creativity_df.columns if 'AF7' in col or 'AF8' in col]
    df['Creativity_Frontal'] = creativity_df[creativity_frontal_cols].mean(axis=1)
   # df['Creativity_Frontal'] = (df['Creativity_Frontal'] / df['Creativity_Frontal'].max()) * 100

    # Calculate Creativity_Posterior, normalize to show as percentage, and add it to the original DataFrame
    creativity_posterior_cols = [col for col in creativity_df.columns if 'TP9' in col or 'TP10' in col]
    df['Creativity_Posterior'] = creativity_df[creativity_posterior_cols].mean(axis=1)
    #df['Creativity_Posterior'] = (df['Creativity_Posterior'] / df['Creativity_Posterior'].max()) * 100

    # Apply Min-Max normalization to the creativity metrics
    for col in ['Creativity_AVG','Creativity_Frontal', 'Creativity_Posterior']:
        # df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())*100
        df[col] = (df[col]  / df[col].max() )*100


def add_relaxation_metrics(df):
    """
    Adds relaxation metrics by converting theta and alpha power values from dB to a linear scale,
    then dividing theta power columns by alpha columns for each sensor, and calculates average,
    frontal, and posterior relaxation metrics with Min-Max normalization.
    """
    # Initialize a temporary DataFrame for relaxation calculations
    relaxation_df = pd.DataFrame()

    # Convert Theta and Alpha power values from dB to linear scale and calculate Theta/Alpha for each sensor
    for theta_col, alpha_col in zip(theta_cols, alpha_cols):
        # theta_linear = 10 ** (df[theta_col] )
        # alpha_linear = 10 ** (df[alpha_col] )
        relaxation_col = f'Relaxation_{theta_col.split("_")[1]}'
        relaxation_df[relaxation_col] = df[theta_col] / df[alpha_col]

    # Calculate Relaxation_AVG and add it to the original DataFrame
    df['Relaxation_AVG'] = relaxation_df.mean(axis=1)

    # Calculate Relaxation_Frontal and Relaxation_Posterior
    relaxation_frontal_cols = [col for col in relaxation_df.columns if 'AF7' in col or 'AF8' in col]
    df['Relaxation_Frontal'] = relaxation_df[relaxation_frontal_cols].mean(axis=1)
    
    relaxation_posterior_cols = [col for col in relaxation_df.columns if 'TP9' in col or 'TP10' in col]
    df['Relaxation_Posterior'] = relaxation_df[relaxation_posterior_cols].mean(axis=1)

    # Apply Min-Max normalization to the relaxation metrics
    for col in ['Relaxation_AVG', 'Relaxation_Frontal', 'Relaxation_Posterior']:
        #df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
        df[col] = (df[col]  / df[col].max() )*100

def add_relaxation_metrics_2(df):
    """
    Adds relaxation metrics by converting theta and alpha power values from dB to a linear scale,
    then dividing theta power columns by alpha columns for each sensor, and calculates average,
    frontal, and posterior relaxation metrics with Min-Max normalization.
    """
    # Initialize a temporary DataFrame for relaxation calculations
    relaxation_df = pd.DataFrame()

    # Convert Theta and Alpha power values from dB to linear scale and calculate Theta/Alpha for each sensor
    for alpha_col, beta_col in zip( alpha_cols, beta_cols):
        # alpha_linear = 10 ** (df[alpha_col] )
        # beta_linear = 10 ** (df[beta_col] )
        relaxation_col = f'Relaxation2_{alpha_col.split("_")[1]}'
        relaxation_df[relaxation_col] = df[alpha_col] / df[beta_col]

    # Calculate Relaxation_AVG and add it to the original DataFrame
    df['Relaxation2_AVG'] = relaxation_df.mean(axis=1)

    # Calculate Relaxation_Frontal and Relaxation_Posterior
    relaxation_frontal_cols = [col for col in relaxation_df.columns if 'AF7' in col or 'AF8' in col]
    df['Relaxation2_Frontal'] = relaxation_df[relaxation_frontal_cols].mean(axis=1)
    
    relaxation_posterior_cols = [col for col in relaxation_df.columns if 'TP9' in col or 'TP10' in col]
    df['Relaxation2_Posterior'] = relaxation_df[relaxation_posterior_cols].mean(axis=1)

    # Apply Min-Max normalization to the relaxation metrics
    for col in ['Relaxation2_AVG', 'Relaxation2_Frontal', 'Relaxation2_Posterior']:
        # df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
        df[col] = (df[col]  / df[col].max() )*100


def add_regeneration_metrics(df):
    """
    Adds regeneration metrics by converting alpha and delta power values from dB to a linear scale,
    then dividing alpha power columns by delta columns for each sensor, and calculates average,
    frontal, and posterior regeneration metrics with Min-Max normalization.
    """
    # Initialize a temporary DataFrame for regeneration calculations
    regeneration_df = pd.DataFrame()

    # Convert Alpha and Delta power values from dB to linear scale and calculate Alpha/Delta for each sensor
    for alpha_col, delta_col in zip(alpha_cols, delta_cols):
        # alpha_linear = 10 ** (df[alpha_col] )
        # delta_linear = 10 ** (df[delta_col] )
        regeneration_col = f'Regeneration_{alpha_col.split("_")[1]}'
        regeneration_df[regeneration_col] = df[alpha_col] / df[delta_col]

    # Calculate Regeneration_AVG and add it to the original DataFrame
    df['Regeneration_AVG'] = regeneration_df.mean(axis=1)

    # Calculate Regeneration_Frontal and Regeneration_Posterior
    regeneration_frontal_cols = [col for col in regeneration_df.columns if 'AF7' in col or 'AF8' in col]
    df['Regeneration_Frontal'] = regeneration_df[regeneration_frontal_cols].mean(axis=1)
    
    regeneration_posterior_cols = [col for col in regeneration_df.columns if 'TP9' in col or 'TP10' in col]
    df['Regeneration_Posterior'] = regeneration_df[regeneration_posterior_cols].mean(axis=1)

    # Apply Min-Max normalization to the regeneration metrics
    for col in ['Regeneration_AVG', 'Regeneration_Frontal', 'Regeneration_Posterior']:
        # df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
        df[col] = (df[col]  / df[col].max() )*100


def add_engagement_metrics(df):
    """
    Adds engagement metrics by converting beta, alpha, and theta power values from dB to a linear scale,
    then dividing beta power columns by the sum of alpha and theta columns for each sensor, and calculates
    average, frontal, and posterior engagement metrics with Min-Max normalization.
    """
    # Initialize a temporary DataFrame for engagement calculations
    engagement_df = pd.DataFrame()

    # Convert Beta, Alpha, and Theta power values from dB to linear scale and calculate Beta / (Alpha + Theta) for each sensor
    for beta_col, alpha_col, theta_col in zip(beta_cols, alpha_cols, theta_cols):
        # beta_linear = 10 ** (df[beta_col] )
        # alpha_linear = 10 ** (df[alpha_col] )
        # theta_linear = 10 ** (df[theta_col] )
        engagement_col = f'Engagement_{beta_col.split("_")[1]}'
        engagement_df[engagement_col] = df[beta_col] / (df[alpha_col] + df[theta_col])

    # Calculate Engagement_AVG and add it to the original DataFrame
    df['Engagement_AVG'] = engagement_df.mean(axis=1)

    # Calculate Engagement_Frontal and Engagement_Posterior
    engagement_frontal_cols = [col for col in engagement_df.columns if 'AF7' in col or 'AF8' in col]
    df['Engagement_Frontal'] = engagement_df[engagement_frontal_cols].mean(axis=1)
    
    engagement_posterior_cols = [col for col in engagement_df.columns if 'TP9' in col or 'TP10' in col]
    df['Engagement_Posterior'] = engagement_df[engagement_posterior_cols].mean(axis=1)

    # Apply Min-Max normalization to the engagement metrics
    for col in ['Engagement_AVG', 'Engagement_Frontal', 'Engagement_Posterior']:
        # df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
        df[col] = (df[col]  / df[col].max() )*100


def add_engagement_metrics_v2(df):
    """
    Adds engagement metrics using the formula (Delta + Theta) / (Beta + Alpha) for each sensor,
    then calculates average, frontal, and posterior engagement metrics with Min-Max normalization.
    """
    # Initialize a temporary DataFrame for engagement calculations
    engagement_df_v2 = pd.DataFrame()

    # Convert power values from dB to linear scale for necessary bands
    for delta_col, theta_col, alpha_col, beta_col in zip(delta_cols, theta_cols, alpha_cols, beta_cols):
        # delta_linear = 10 ** (df[delta_col] )
        # theta_linear = 10 ** (df[theta_col] )
        # alpha_linear = 10 ** (df[alpha_col] )
        # beta_linear = 10 ** (df[beta_col] )
        
        engagement_col_v2 = f'EngagementV2_{delta_col.split("_")[1]}'
        engagement_df_v2[engagement_col_v2] = (df[delta_col] + df[theta_col]) / (df[beta_col] + df[alpha_col])

    # Calculate EngagementV2_AVG and add it to the original DataFrame
    df['EngagementV2_AVG'] = engagement_df_v2.mean(axis=1)

    # Calculate EngagementV2_Frontal and EngagementV2_Posterior
    engagement_frontal_cols_v2 = [col for col in engagement_df_v2.columns if 'AF7' in col or 'AF8' in col]
    df['EngagementV2_Frontal'] = engagement_df_v2[engagement_frontal_cols_v2].mean(axis=1)
    
    engagement_posterior_cols_v2 = [col for col in engagement_df_v2.columns if 'TP9' in col or 'TP10' in col]
    df['EngagementV2_Posterior'] = engagement_df_v2[engagement_posterior_cols_v2].mean(axis=1)

    # Apply Min-Max normalization to the engagement metrics
    for col in ['EngagementV2_AVG', 'EngagementV2_Frontal', 'EngagementV2_Posterior']:
        # df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
        df[col] = (df[col]  / df[col].max() )*100




