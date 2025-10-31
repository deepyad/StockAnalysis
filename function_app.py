import azure.functions as func
import logging
import os
import datetime
from datetime import datetime
from StockAnalyser_Final import process_holdings_file
from azure.functions import TimerRequest
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import json

app = func.FunctionApp()

@app.timer_trigger(schedule="0 0 9 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def StockAnalysisTimer(myTimer: func.TimerRequest) -> None:
    """
    Runs daily at 9:00 AM IST (adjust timezone as needed)
    Schedule format: "0 0 9 * * *" = minute=0, hour=9, every day
    To run at 6 PM IST: "0 0 18 * * *"
    """
    utc_timestamp = datetime.utcnow().replace(tzinfo=None).isoformat()
    
    if myTimer.past_due:
        logging.info('The timer is past due!')
    
    logging.info(f'StockAnalysisTimer function ran at {utc_timestamp}')
    
    try:
        # Run the stock analysis
        logging.info("Starting stock analysis...")
        
        # Generate timestamped output filename
        now = datetime.now()
        output_file = f"OUTPUT_{now.strftime('%d_%b_%Y')}_{now.strftime('%H%M%S')}.xlsx"
        
        # Run analysis (modify path as needed)
        process_holdings_file(
            input_file="./holdings_with_changes_14_Aug.csv",
            output_file=output_file
        )
        
        logging.info(f"Analysis complete. Output saved to {output_file}")
        
        # Send email with output file
        send_email_with_attachment(output_file)
        
        logging.info("Email sent successfully")
        
    except Exception as e:
        error_msg = f"Error in StockAnalysisTimer: {str(e)}"
        logging.error(error_msg)
        send_error_email(error_msg)

@app.function_name(name="StockAnalysisManual")
@app.route(route="run", auth_level=func.AuthLevel.ANONYMOUS)
def StockAnalysisManual(req: func.HttpRequest) -> func.HttpResponse:
    """
    Manual trigger endpoint: POST to your-function-app.azurewebsites.net/api/run
    Can be called from other services, GitHub Actions, etc.
    """
    try:
        logging.info("Manual trigger received")
        
        # Generate timestamped output filename
        now = datetime.now()
        output_file = f"OUTPUT_{now.strftime('%d_%b_%Y')}_{now.strftime('%H%M%S')}.xlsx"
        
        # Run analysis
        process_holdings_file(
            input_file="./holdings_with_changes_14_Aug.csv",
            output_file=output_file
        )
        
        # Send email with output file
        send_email_with_attachment(output_file)
        
        return func.HttpResponse(
            f"Stock analysis completed successfully. Output: {output_file}",
            status_code=200
        )
        
    except Exception as e:
        error_msg = f"Error in manual run: {str(e)}"
        logging.error(error_msg)
        send_error_email(error_msg)
        return func.HttpResponse(error_msg, status_code=500)

def send_email_with_attachment(filename):
    """
    Send email with the generated Excel file attached
    Configure email settings via Azure Function App Settings
    """
    try:
        # Email configuration from environment variables
        smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        sender_email = os.environ.get('SENDER_EMAIL')  # Your email
        sender_password = os.environ.get('SENDER_PASSWORD')  # App password
        recipient_email = os.environ.get('RECIPIENT_EMAIL')  # Your email
        
        if not all([sender_email, sender_password, recipient_email]):
            logging.error("Email configuration missing in environment variables")
            return
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"Stock Analysis Report - {datetime.now().strftime('%d %b %Y %H:%M')}"
        
        body = f"""
        Hello,
        
        Please find attached the daily stock analysis report.
        
        Generated on: {datetime.now().strftime('%d %b %Y at %H:%M IST')}
        
        Best regards,
        Stock Analysis Bot
        """
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach file
        if os.path.exists(filename):
            with open(filename, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {filename}',
                )
                msg.attach(part)
        else:
            logging.warning(f"File not found: {filename}")
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            
        logging.info("Email sent successfully")
        
    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")

def send_error_email(error_message):
    """
    Send error notification email
    """
    try:
        smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        sender_email = os.environ.get('SENDER_EMAIL')
        sender_password = os.environ.get('SENDER_PASSWORD')
        recipient_email = os.environ.get('RECIPIENT_EMAIL')
        
        if not all([sender_email, sender_password, recipient_email]):
            logging.error("Email configuration missing")
            return
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "Stock Analysis Error Alert"
        
        body = f"""
        Error occurred in Stock Analysis Function:
        
        {error_message}
        
        Time: {datetime.now().strftime('%d %b %Y %H:%M IST')}
        """
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            
    except Exception as e:
        logging.error(f"Error sending error email: {str(e)}")

