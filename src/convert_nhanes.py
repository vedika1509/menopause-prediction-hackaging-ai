import pandas as pd
import os
import glob
from pathlib import Path

def convert_xpt_to_csv():
    """
    Convert all .xpt files from NHANES raw data to a unified CSV file.
    """
    # Define paths
    raw_data_path = "data/raw/NHANES"
    processed_path = "data/processed/NHANES"
    
    # Create processed directory if it doesn't exist
    os.makedirs(processed_path, exist_ok=True)
    
    # Find all .xpt files recursively
    xpt_files = glob.glob(os.path.join(raw_data_path, "**", "*.xpt"), recursive=True)
    
    print(f"Found {len(xpt_files)} .xpt files to process...")
    
    # List to store all dataframes
    all_dataframes = []
    file_info = []
    
    for file_path in xpt_files:
        try:
            print(f"Processing: {file_path}")
            
            # Read the .xpt file
            df = pd.read_sas(file_path)
            
            # Add source file information
            df['source_file'] = os.path.basename(file_path)
            df['source_category'] = os.path.basename(os.path.dirname(file_path))
            
            # Store file info
            file_info.append({
                'file_name': os.path.basename(file_path),
                'category': os.path.basename(os.path.dirname(file_path)),
                'rows': len(df),
                'columns': len(df.columns)
            })
            
            all_dataframes.append(df)
            print(f"  - Loaded {len(df)} rows, {len(df.columns)} columns")
            
        except Exception as e:
            print(f"  - Error processing {file_path}: {str(e)}")
            continue
    
    if not all_dataframes:
        print("No dataframes were successfully loaded!")
        return
    
    # Combine all dataframes
    print("\nCombining all dataframes...")
    unified_df = pd.concat(all_dataframes, ignore_index=True, sort=False)
    
    print(f"Unified dataset shape: {unified_df.shape}")
    
    # Save the unified CSV with compression to handle large file size
    output_file = os.path.join(processed_path, "nhanes_unified.csv")
    try:
        unified_df.to_csv(output_file, index=False)
        print(f"Saved unified dataset to: {output_file}")
    except PermissionError:
        # Try saving with compression
        output_file_compressed = os.path.join(processed_path, "nhanes_unified.csv.gz")
        unified_df.to_csv(output_file_compressed, index=False, compression='gzip')
        print(f"Saved compressed unified dataset to: {output_file_compressed}")
    except Exception as e:
        print(f"Error saving unified dataset: {str(e)}")
        # Save a sample for testing
        sample_file = os.path.join(processed_path, "nhanes_sample.csv")
        unified_df.head(10000).to_csv(sample_file, index=False)
        print(f"Saved sample dataset (10k rows) to: {sample_file}")
    
    # Save file information
    file_info_df = pd.DataFrame(file_info)
    info_file = os.path.join(processed_path, "nhanes_file_info.csv")
    file_info_df.to_csv(info_file, index=False)
    print(f"Saved file information to: {info_file}")
    
    # Print summary statistics
    print("\n=== Summary ===")
    print(f"Total files processed: {len(file_info)}")
    print(f"Total rows in unified dataset: {len(unified_df)}")
    print(f"Total columns in unified dataset: {len(unified_df.columns)}")
    
    # Show category breakdown
    category_counts = unified_df['source_category'].value_counts()
    print("\nCategory breakdown:")
    for category, count in category_counts.items():
        print(f"  {category}: {count} rows")
    
    return unified_df

if __name__ == "__main__":
    convert_xpt_to_csv()
