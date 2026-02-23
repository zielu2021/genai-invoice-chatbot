import sqlite3
from datetime import datetime, timedelta
from typing import Optional
import re

class InvoiceChatbot:
    def __init__(self, db_path: str = "database/invoices.db"):
        self.db_path = db_path
        self.context = {}
        self.commands = {
            "help": self.show_help,
            "status": self.get_invoice_status,
            "search": self.search_invoices,
            "overdue": self.get_overdue_invoices,
            "summary": self.get_summary,
            "client": self.get_client_info,
            "remind": self.send_reminder,
            "analytics": self.get_analytics,
            "recent": self.get_recent_invoices,
            "products": self.get_top_products,
        }
    
    def connect(self):
        return sqlite3.connect(self.db_path)
    
    def process_message(self, message: str) -> str:
        """Main entry point for processing user messages."""
        message = message.strip().lower()
        
        # Check for greetings
        if any(greet in message for greet in ["hello", "hi", "hey", "good morning", "good afternoon"]):
            return self._greeting_response()
        
        # Check for command patterns
        for cmd, handler in self.commands.items():
            if cmd in message:
                return handler(message)
        
        # Natural language processing
        return self._nlp_response(message)
    
    def _greeting_response(self) -> str:
        return """👋 Hello! I'm your Invoice Assistant. Here's what I can help you with:

📊 **Quick Commands:**
• `status INV-2024-001` - Check invoice status
• `overdue` - View overdue invoices
• `summary` - Get financial summary
• `analytics` - View business analytics
• `recent` - See recent invoices
• `help` - Full command list

Just type your question naturally, and I'll assist you!"""

    def show_help(self, _) -> str:
        return """📚 **Available Commands:**

**Invoice Management:**
• `status [invoice#]` - Check specific invoice
• `search [term]` - Search invoices
• `recent` - Last 5 invoices
• `overdue` - Overdue invoices

**Client Info:**
• `client [name]` - Client details & history

**Reports:**
• `summary` - Financial overview
• `analytics` - Business insights
• `products` - Top selling products

**Actions:**
• `remind [invoice#]` - Generate reminder

💡 *Tip: You can also ask naturally, e.g., "How much does Acme owe?"*"""

    def get_invoice_status(self, message: str) -> str:
        # Extract invoice number
        match = re.search(r'INV-\d{4}-\d{3}', message.upper())
        if not match:
            return "❌ Please provide an invoice number (e.g., `status INV-2024-001`)"
        
        invoice_num = match.group()
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT i.*, c.name as client_name, c.email
            FROM invoices i
            JOIN clients c ON i.client_id = c.id
            WHERE i.invoice_number = ?
        """, (invoice_num,))
        
        invoice = cursor.fetchone()
        conn.close()
        
        if not invoice:
            return f"❌ Invoice {invoice_num} not found."
        
        status_emoji = {"paid": "✅", "pending": "⏳", "overdue": "🔴", "draft": "📝", "cancelled": "❌"}
        
        return f"""📄 **Invoice {invoice_num}**

👤 **Client:** {invoice[8]} ({invoice[9]})
📅 **Issued:** {invoice[3]}
⏰ **Due:** {invoice[4]}
💰 **Amount:** ${invoice[6]:,.2f}
📌 **Status:** {status_emoji.get(invoice[5], '❓')} {invoice[5].upper()}
📝 **Notes:** {invoice[7] or 'None'}"""

    def get_overdue_invoices(self, _) -> str:
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT i.invoice_number, c.name, i.total_amount, i.due_date,
                   julianday('now') - julianday(i.due_date) as days_overdue
            FROM invoices i
            JOIN clients c ON i.client_id = c.id
            WHERE i.status = 'overdue' OR (i.status = 'pending' AND i.due_date < date('now'))
            ORDER BY days_overdue DESC
        """)
        
        invoices = cursor.fetchall()
        conn.close()
        
        if not invoices:
            return "✅ Great news! No overdue invoices."
        
        total_overdue = sum(inv[2] for inv in invoices)
        
        result = f"🔴 **Overdue Invoices ({len(invoices)})**\n"
        result += f"💰 Total Outstanding: **${total_overdue:,.2f}**\n\n"
        
        for inv in invoices:
            days = int(inv[4])
            result += f"• **{inv[0]}** - {inv[1]}\n  ${inv[2]:,.2f} | {days} days overdue\n"
        
        return result

    def get_summary(self, _) -> str:
        conn = self.connect()
        cursor = conn.cursor()
        
        # Get totals by status
        cursor.execute("""
            SELECT status, COUNT(*), COALESCE(SUM(total_amount), 0)
            FROM invoices
            GROUP BY status
        """)
        status_data = {row[0]: (row[1], row[2]) for row in cursor.fetchall()}
        
        # Get this month's revenue
        cursor.execute("""
            SELECT COALESCE(SUM(total_amount), 0)
            FROM invoices
            WHERE status = 'paid' AND strftime('%Y-%m', issue_date) = strftime('%Y-%m', 'now')
        """)
        monthly_revenue = cursor.fetchone()[0]
        
        conn.close()
        
        paid = status_data.get('paid', (0, 0))
        pending = status_data.get('pending', (0, 0))
        overdue = status_data.get('overdue', (0, 0))
        
        return f"""📊 **Financial Summary**

**This Month:**
💵 Revenue: **${monthly_revenue:,.2f}**

**All Time:**
✅ Paid: {paid[0]} invoices (${paid[1]:,.2f})
⏳ Pending: {pending[0]} invoices (${pending[1]:,.2f})
🔴 Overdue: {overdue[0]} invoices (${overdue[1]:,.2f})

**Total Outstanding:** ${pending[1] + overdue[1]:,.2f}"""

    def get_analytics(self, _) -> str:
        conn = self.connect()
        cursor = conn.cursor()
        
        # Top clients by revenue
        cursor.execute("""
            SELECT c.name, SUM(i.total_amount) as total
            FROM invoices i
            JOIN clients c ON i.client_id = c.id
            WHERE i.status = 'paid'
            GROUP BY c.id
            ORDER BY total DESC
            LIMIT 3
        """)
        top_clients = cursor.fetchall()
        
        # Average invoice value
        cursor.execute("SELECT AVG(total_amount) FROM invoices WHERE status != 'cancelled'")
        avg_invoice = cursor.fetchone()[0] or 0
        
        # Payment rate
        cursor.execute("""
            SELECT 
                COUNT(CASE WHEN status = 'paid' THEN 1 END) * 100.0 / COUNT(*)
            FROM invoices WHERE status != 'draft' AND status != 'cancelled'
        """)
        payment_rate = cursor.fetchone()[0] or 0
        
        conn.close()
        
        result = f"""📈 **Business Analytics**

**Top Clients by Revenue:**
"""
        for i, (name, total) in enumerate(top_clients, 1):
            result += f"  {i}. {name}: ${total:,.2f}\n"
        
        result += f"""
**Key Metrics:**
📊 Avg Invoice Value: **${avg_invoice:,.2f}**
✅ Payment Rate: **{payment_rate:.1f}%**"""
        
        return result

    def get_client_info(self, message: str) -> str:
        # Extract client name
        words = message.replace("client", "").strip().split()
        if not words:
            return "❌ Please provide a client name (e.g., `client Acme`)"
        
        search_term = " ".join(words)
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM clients WHERE LOWER(name) LIKE ?
        """, (f"%{search_term}%",))
        
        client = cursor.fetchone()
        
        if not client:
            return f"❌ No client found matching '{search_term}'"
        
        # Get client's invoices
        cursor.execute("""
            SELECT invoice_number, status, total_amount, issue_date
            FROM invoices WHERE client_id = ?
            ORDER BY issue_date DESC
        """, (client[0],))
        invoices = cursor.fetchall()
        
        conn.close()
        
        total_billed = sum(inv[2] for inv in invoices)
        
        result = f"""👤 **{client[1]}**

📧 {client[2]}
📞 {client[3]}
📍 {client[4]}

**Invoice History:** ({len(invoices)} total, ${total_billed:,.2f} billed)
"""
        for inv in invoices[:5]:
            status_emoji = {"paid": "✅", "pending": "⏳", "overdue": "🔴", "draft": "📝"}
            result += f"• {inv[0]} - {status_emoji.get(inv[1], '❓')} ${inv[2]:,.2f}\n"
        
        return result

    def get_recent_invoices(self, _) -> str:
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT i.invoice_number, c.name, i.total_amount, i.status, i.issue_date
            FROM invoices i
            JOIN clients c ON i.client_id = c.id
            ORDER BY i.issue_date DESC
            LIMIT 5
        """)
        
        invoices = cursor.fetchall()
        conn.close()
        
        result = "📋 **Recent Invoices**\n\n"
        for inv in invoices:
            status_emoji = {"paid": "✅", "pending": "⏳", "overdue": "🔴", "draft": "📝", "cancelled": "❌"}
            result += f"• **{inv[0]}** - {inv[1]}\n  ${inv[2]:,.2f} | {status_emoji.get(inv[3], '❓')} {inv[3]} | {inv[4]}\n\n"
        
        return result

    def get_top_products(self, _) -> str:
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT p.name, SUM(ii.quantity) as qty, SUM(ii.quantity * ii.unit_price) as revenue
            FROM invoice_items ii
            JOIN products p ON ii.product_id = p.id
            GROUP BY p.id
            ORDER BY revenue DESC
            LIMIT 5
        """)
        
        products = cursor.fetchall()
        conn.close()
        
        result = "🏆 **Top Products by Revenue**\n\n"
        for i, (name, qty, revenue) in enumerate(products, 1):
            result += f"{i}. **{name}**\n   {qty} sold | ${revenue:,.2f} revenue\n\n"
        
        return result

    def send_reminder(self, message: str) -> str:
        match = re.search(r'INV-\d{4}-\d{3}', message.upper())
        if not match:
            return "❌ Please provide an invoice number (e.g., `remind INV-2024-004`)"
        
        invoice_num = match.group()
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT i.*, c.name, c.email
            FROM invoices i
            JOIN clients c ON i.client_id = c.id
            WHERE i.invoice_number = ?
        """, (invoice_num,))
        
        invoice = cursor.fetchone()
        conn.close()
        
        if not invoice:
            return f"❌ Invoice {invoice_num} not found."
        
        return f"""📧 **Payment Reminder Generated**

**To:** {invoice[9]}
**Subject:** Payment Reminder - Invoice {invoice_num}

---
Dear {invoice[8]},

This is a friendly reminder that invoice **{invoice_num}** for **${invoice[6]:,.2f}** was due on **{invoice[4]}**.

Please arrange payment at your earliest convenience.

Best regards,
Accounts Team
---

*Copy this message and send via your email client.*"""

    def search_invoices(self, message: str) -> str:
        search_term = message.replace("search", "").strip()
        if not search_term:
            return "❌ Please provide a search term (e.g., `search Acme`)"
        
        conn = self.connect()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT i.invoice_number, c.name, i.total_amount, i.status
            FROM invoices i
            JOIN clients c ON i.client_id = c.id
            WHERE LOWER(c.name) LIKE ? OR LOWER(i.invoice_number) LIKE ? OR LOWER(i.notes) LIKE ?
        """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return f"❌ No invoices found for '{search_term}'"
        
        result = f"🔍 **Search Results for '{search_term}'** ({len(results)} found)\n\n"
        for inv in results:
            status_emoji = {"paid": "✅", "pending": "⏳", "overdue": "🔴", "draft": "📝", "cancelled": "❌"}
            result += f"• **{inv[0]}** - {inv[1]} | ${inv[2]:,.2f} | {status_emoji.get(inv[3], '❓')}\n"
        
        return result

    def _nlp_response(self, message: str) -> str:
        """Handle natural language queries."""
        # Amount/owe queries
        if any(word in message for word in ["owe", "owes", "outstanding", "unpaid"]):
            return self.get_overdue_invoices(message)
        
        # Revenue queries
        if any(word in message for word in ["revenue", "earned", "made", "income"]):
            return self.get_summary(message)
        
        # Client queries
        if "client" in message or "customer" in message:
            return self.get_client_info(message)
        
        return """🤔 I'm not sure I understand. Try:
• `help` - See all commands
• `summary` - Financial overview
• `status INV-2024-001` - Check specific invoice

Or ask me something like "Who owes us money?" or "Show recent invoices"."""


# Main execution
if __name__ == "__main__":
    bot = InvoiceChatbot()
    print("🤖 Invoice Chatbot Ready! Type 'quit' to exit.\n")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Goodbye!")
            break
        
        response = bot.process_message(user_input)
        print(f"\nBot: {response}\n")
