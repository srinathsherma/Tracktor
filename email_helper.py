# email_helper.py
from flask_mail import Mail, Message
from flask import current_app

mail = Mail()

def send_ticket_assigned_email(technician, ticket):
    """Send email to technician when a ticket is assigned to them"""
    try:
        msg = Message(
            subject = f'🚜 Tracktor — New ticket assigned to you: {ticket.title}',
            recipients = [technician.email]
        )
        msg.html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px;
                    margin: 0 auto; background: #FFF8E1;
                    border: 1px solid #E0C050; border-radius: 10px;
                    overflow: hidden;">

            <!-- Header -->
            <div style="background: #B8860B; padding: 24px 32px;">
                <h1 style="color: white; margin: 0; font-size: 24px;">
                    🚜 Tracktor
                </h1>
                <p style="color: #FFD966; margin: 4px 0 0; font-size: 14px;">
                    Issue Tracking System
                </p>
            </div>

            <!-- Body -->
            <div style="padding: 32px;">
                <h2 style="color: #B8860B; margin-top: 0;">
                    Hi {technician.name}! 👋
                </h2>
                <p style="color: #333; font-size: 15px; line-height: 1.6;">
                    A new ticket has been assigned to you in Tracktor.
                    Please review the details below and take action as soon
                    as possible.
                </p>

                <!-- Ticket details card -->
                <div style="background: white; border: 1px solid #E0C050;
                            border-radius: 8px; padding: 24px;
                            margin: 24px 0;">

                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px 0; font-size: 13px;
                                       color: #777; width: 140px;
                                       font-weight: bold;">
                                Ticket #
                            </td>
                            <td style="padding: 8px 0; font-size: 14px;
                                       color: #333;">
                                {ticket.id}
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-size: 13px;
                                       color: #777; font-weight: bold;">
                                Title
                            </td>
                            <td style="padding: 8px 0; font-size: 14px;
                                       color: #333; font-weight: bold;">
                                {ticket.title}
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-size: 13px;
                                       color: #777; font-weight: bold;">
                                Priority
                            </td>
                            <td style="padding: 8px 0;">
                                <span style="
                                    padding: 4px 10px;
                                    border-radius: 12px;
                                    font-size: 12px;
                                    font-weight: bold;
                                    background: {'#C0392B' if ticket.priority == 'critical' else '#E67E22' if ticket.priority == 'high' else '#2980B9' if ticket.priority == 'medium' else '#27AE60'};
                                    color: white;">
                                    {ticket.priority.title()}
                                </span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-size: 13px;
                                       color: #777; font-weight: bold;">
                                Category
                            </td>
                            <td style="padding: 8px 0; font-size: 14px;
                                       color: #333;">
                                {ticket.category.name if ticket.category else '— uncategorised —'}
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-size: 13px;
                                       color: #777; font-weight: bold;">
                                Description
                            </td>
                            <td style="padding: 8px 0; font-size: 14px;
                                       color: #333; line-height: 1.6;">
                                {ticket.description}
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-size: 13px;
                                       color: #777; font-weight: bold;">
                                Date requested
                            </td>
                            <td style="padding: 8px 0; font-size: 14px;
                                       color: #333;">
                                {ticket.date_requested.strftime('%d %b %Y, %I:%M %p')}
                            </td>
                        </tr>
                    </table>
                </div>

                <!-- Notes section -->
                {% if ticket.notes %}
                <div style="background: #FEF9E7; border-left: 4px solid #B8860B;
                            padding: 16px; border-radius: 0 8px 8px 0;
                            margin-bottom: 24px;">
                    <p style="margin: 0; font-size: 13px; color: #777;
                               font-weight: bold;">Notes</p>
                    <p style="margin: 8px 0 0; font-size: 14px; color: #333;">
                        {ticket.notes}
                    </p>
                </div>
                {% endif %}

                <p style="color: #333; font-size: 14px; line-height: 1.6;">
                    Please log in to Tracktor to update the ticket status
                    and add any notes as you work on this issue.
                </p>

            </div>

            <!-- Footer -->
            <div style="background: #F5E88A; padding: 16px 32px;
                        border-top: 1px solid #E0C050;">
                <p style="margin: 0; font-size: 12px; color: #777;
                           text-align: center;">
                    This email was sent by 🚜 Tracktor — Issue Tracking System
                </p>
            </div>

        </div>
        """

        from app import mail as app_mail
        app_mail.send(msg)
        print(f"✅ Email sent to {technician.email}")
        return True

    except Exception as e:
        print(f"❌ Email failed: {str(e)}")
        return False


def send_ticket_closed_email(technician, ticket):
    """Send email to technician when a ticket is closed"""
    try:
        msg = Message(
            subject = f'🚜 Tracktor — Ticket closed: {ticket.title}',
            recipients = [technician.email]
        )
        msg.html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px;
                    margin: 0 auto; background: #FFF8E1;
                    border: 1px solid #E0C050; border-radius: 10px;
                    overflow: hidden;">

            <!-- Header -->
            <div style="background: #27AE60; padding: 24px 32px;">
                <h1 style="color: white; margin: 0; font-size: 24px;">
                    🚜 Tracktor
                </h1>
                <p style="color: #EAFAF1; margin: 4px 0 0; font-size: 14px;">
                    Issue Tracking System
                </p>
            </div>

            <!-- Body -->
            <div style="padding: 32px;">
                <h2 style="color: #27AE60; margin-top: 0;">
                    Ticket closed! ✅
                </h2>
                <p style="color: #333; font-size: 15px; line-height: 1.6;">
                    Hi {technician.name}! The following ticket has been
                    marked as closed in Tracktor.
                </p>

                <!-- Ticket details card -->
                <div style="background: white; border: 1px solid #E0C050;
                            border-radius: 8px; padding: 24px;
                            margin: 24px 0;">
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px 0; font-size: 13px;
                                       color: #777; width: 140px;
                                       font-weight: bold;">
                                Ticket #
                            </td>
                            <td style="padding: 8px 0; font-size: 14px;
                                       color: #333;">
                                {ticket.id}
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-size: 13px;
                                       color: #777; font-weight: bold;">
                                Title
                            </td>
                            <td style="padding: 8px 0; font-size: 14px;
                                       color: #333; font-weight: bold;">
                                {ticket.title}
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-size: 13px;
                                       color: #777; font-weight: bold;">
                                Date requested
                            </td>
                            <td style="padding: 8px 0; font-size: 14px;
                                       color: #333;">
                                {ticket.date_requested.strftime('%d %b %Y, %I:%M %p')}
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-size: 13px;
                                       color: #777; font-weight: bold;">
                                Date completed
                            </td>
                            <td style="padding: 8px 0; font-size: 14px;
                                       color: #333;">
                                {ticket.date_completed.strftime('%d %b %Y, %I:%M %p') if ticket.date_completed else '—'}
                            </td>
                        </tr>
                    </table>
                </div>

                <p style="color: #333; font-size: 14px; line-height: 1.6;">
                    Great work resolving this ticket! 🎉
                </p>
            </div>

            <!-- Footer -->
            <div style="background: #F5E88A; padding: 16px 32px;
                        border-top: 1px solid #E0C050;">
                <p style="margin: 0; font-size: 12px; color: #777;
                           text-align: center;">
                    This email was sent by 🚜 Tracktor — Issue Tracking System
                </p>
            </div>

        </div>
        """

        from app import mail as app_mail
        app_mail.send(msg)
        print(f"✅ Closed email sent to {technician.email}")
        return True

    except Exception as e:
        print(f"❌ Email failed: {str(e)}")
        return False


def send_critical_ticket_email(technicians, ticket):
    """Send email to all technicians when a critical ticket is created"""
    try:
        recipients = [tech.email for tech in technicians]
        msg = Message(
            subject = f'🔴 Tracktor — Critical ticket: {ticket.title}',
            recipients = recipients
        )
        msg.html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px;
                    margin: 0 auto; background: #FFF8E1;
                    border: 1px solid #E0C050; border-radius: 10px;
                    overflow: hidden;">

            <!-- Header -->
            <div style="background: #C0392B; padding: 24px 32px;">
                <h1 style="color: white; margin: 0; font-size: 24px;">
                    🚜 Tracktor
                </h1>
                <p style="color: #FDECEA; margin: 4px 0 0; font-size: 14px;">
                    Issue Tracking System
                </p>
            </div>

            <!-- Body -->
            <div style="padding: 32px;">
                <h2 style="color: #C0392B; margin-top: 0;">
                    🔴 Critical ticket raised!
                </h2>
                <p style="color: #333; font-size: 15px; line-height: 1.6;">
                    A critical priority ticket has been raised in Tracktor
                    and requires immediate attention!
                </p>

                <!-- Ticket details card -->
                <div style="background: white; border: 1px solid #E0C050;
                            border-radius: 8px; padding: 24px;
                            margin: 24px 0;">
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 8px 0; font-size: 13px;
                                       color: #777; width: 140px;
                                       font-weight: bold;">
                                Ticket #
                            </td>
                            <td style="padding: 8px 0; font-size: 14px;
                                       color: #333;">
                                {ticket.id}
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-size: 13px;
                                       color: #777; font-weight: bold;">
                                Title
                            </td>
                            <td style="padding: 8px 0; font-size: 14px;
                                       color: #333; font-weight: bold;">
                                {ticket.title}
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-size: 13px;
                                       color: #777; font-weight: bold;">
                                Category
                            </td>
                            <td style="padding: 8px 0; font-size: 14px;
                                       color: #333;">
                                {ticket.category.name if ticket.category else '— uncategorised —'}
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-size: 13px;
                                       color: #777; font-weight: bold;">
                                Description
                            </td>
                            <td style="padding: 8px 0; font-size: 14px;
                                       color: #333; line-height: 1.6;">
                                {ticket.description}
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-size: 13px;
                                       color: #777; font-weight: bold;">
                                Date requested
                            </td>
                            <td style="padding: 8px 0; font-size: 14px;
                                       color: #333;">
                                {ticket.date_requested.strftime('%d %b %Y, %I:%M %p')}
                            </td>
                        </tr>
                    </table>
                </div>

                <p style="color: #C0392B; font-size: 14px; font-weight: bold;">
                    ⚠️ Please log in to Tracktor immediately and assign
                    this ticket to a technician!
                </p>
            </div>

            <!-- Footer -->
            <div style="background: #F5E88A; padding: 16px 32px;
                        border-top: 1px solid #E0C050;">
                <p style="margin: 0; font-size: 12px; color: #777;
                           text-align: center;">
                    This email was sent by 🚜 Tracktor — Issue Tracking System
                </p>
            </div>

        </div>
        """

        from app import mail as app_mail
        app_mail.send(msg)
        print(f"✅ Critical ticket email sent to {len(recipients)} technicians!")
        return True

    except Exception as e:
        print(f"❌ Email failed: {str(e)}")
        return False