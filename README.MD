# Automated Currency Exchange Processing

This project automates the process of scheduling, verifying file existence, data transformation, currency amount calculation, importing the latest exchange rates, and generating an analysis report on multi-currency flow direction prediction. It also includes a review mechanism to fine-tune the program for more precise results in the next operational day. The project utilizes Python and Pandas, with processed data saved to a specified directory.

## Table of Contents

- Installation
- Usage
- Configuration
- Features
- Modules
- Contributing
- License

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/sleepySummer/ccy_EarlyWarning.git
    cd auto_DayEnd.git
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Set Up Configuration:**
   - Base Directory: Set the base directory for your project.
   - Paths: Define paths for source and destination folders, target files, and other necessary directories.
   - Currency Lists: Specify the order of currencies and columns for processing.
   - Logging Level: Set the logging level for the application.

2. **Run the Script:**
   - Execute the main script, or scheduler, to start the process:
     ```sh
     python scheduler.py
     ```

## Configuration

## Workflow
1.Download from TTL:

- Navigate to Report Printing -> HKS Front Office - Cash & Stock Balance -> SECFOBAL0106 - Front Office Client Cash and Portfolio Report.
- Set the following options: Format=CSV, Orientation=Landscape, Device=\printsvrn2\Futures, Redirect to=Format Text, Path=desktop, Name=client_bal.
- Click Print.

2.Observation Periods:

- 10:45 AM to 11:15 AM
- 2:45 PM to 3:15 PM
	
3.Place the File:
- Move the "client_bal.csv" file to the target folder: \fsn1\Company Share\FUT_FX\FX\Conversion\Early-warning\temp.

4.Load Latest Data:
- Within 10 seconds, check \fsn1\Company Share\FUT_FX\FX\Conversion\Early-warning\flow_predict_share_ver.xlsm (suggest running on your own machine) and click the button to load the latest data.

5.Review Data:
- Double-check the yellow-highlighted client rows to see if they should be excluded from FXauto Cancelccy.


## License
- Copyright (c) 2024 [Ian Chi]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
