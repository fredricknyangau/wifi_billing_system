import logging
from integrations.services.sms_gateway import SMSGateway
from integrations.services.email_service import EmailService

logger = logging.getLogger(__name__)

class ActionExecutor:
    def __init__(self):
        self.sms_gateway = SMSGateway()
        self.email_service = EmailService()

    def execute_action(self, step, customer):
        """
        Dispatches the action based on step configuration.
        """
        action_type = step.action_type
        config = step.action_config
        
        logger.info(f"Executing action {action_type} for {customer}")
        
        if action_type == 'SEND_SMS':
            phone_number = customer.phone_number
            message = config.get('message', '')
            if phone_number and message:
                return self.sms_gateway.send_sms(phone_number, message)
            
        elif action_type == 'SEND_EMAIL':
            email = customer.user.email
            subject = config.get('subject', '')
            body = config.get('body', '')
            if email and subject and body:
                return self.email_service.send_email(email, subject, body)
                
        elif action_type == 'ASSIGN_TASK':
            # Mock task assignment
            task_name = config.get('task_name', 'General Task')
            print(f"--- TASK ASSIGNED ---\nCustomer: {customer}\nTask: {task_name}\n---------------------")
            return True
            
        elif action_type == 'WAIT':
            # Logic for waiting would be handled by the engine/scheduler
            return True
            
        return False
