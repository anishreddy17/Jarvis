"""
Sample data for testing the Jarvis AI Assistant
"""

SAMPLE_DOCUMENTS = [
    {
        "name": "Company Overview",
        "text": """
        TechCorp is a leading software company founded in 2015. We specialize in enterprise 
        solutions for cloud computing, artificial intelligence, and data analytics. Our mission 
        is to empower businesses with cutting-edge technology.
        
        Our headquarters is located in San Francisco, California, with offices in New York, 
        London, and Tokyo. We employ over 5,000 people worldwide and serve more than 10,000 
        enterprise customers.
        
        Key products include:
        - CloudPlatform: Enterprise cloud infrastructure
        - DataInsights: AI-powered analytics platform
        - SecureConnect: Enterprise security solutions
        """
    },
    {
        "name": "Product Documentation - CloudPlatform",
        "text": """
        CloudPlatform is our flagship product that provides scalable cloud infrastructure 
        for enterprises. Key features include:
        
        1. Auto-scaling: Automatically adjusts resources based on demand
        2. Load Balancing: Distributes traffic across multiple servers
        3. Data Redundancy: Ensures 99.99% uptime with automatic backups
        4. Multi-region Support: Deploy across 20+ global regions
        5. Real-time Monitoring: Track performance with our dashboard
        
        Pricing starts at $500/month for the Basic plan and scales up to Enterprise 
        plans for large organizations. We offer a 30-day free trial for new customers.
        
        Technical Requirements:
        - API access via REST and GraphQL
        - SDK support for Python, Java, JavaScript, and Go
        - Compatible with Docker and Kubernetes
        """
    },
    {
        "name": "HR Policy - Remote Work",
        "text": """
        TechCorp Remote Work Policy (Updated 2024)
        
        All employees are eligible for remote work with manager approval. Key guidelines:
        
        1. Work Hours: Core hours are 10 AM - 3 PM in your timezone
        2. Communication: Daily standup via Slack, weekly team meetings via Zoom
        3. Equipment: Company provides laptop, monitor, and $500 home office stipend
        4. Internet: Minimum 50 Mbps connection required
        5. Availability: Must be reachable during core hours
        
        Hybrid Options:
        - Employees can work 2-3 days from office if they prefer
        - Office space is available on a first-come basis
        - Hot-desking system implemented in all locations
        
        Time Off:
        - 20 days paid vacation per year
        - 10 sick days
        - Flexible holidays based on location
        """
    },
    {
        "name": "Customer Success Story - RetailCo",
        "text": """
        Case Study: How RetailCo Transformed Their Operations with TechCorp
        
        Client: RetailCo - A Fortune 500 retail company
        Challenge: Legacy infrastructure causing downtime and slow performance
        
        Solution Implemented:
        - Migrated to CloudPlatform in Q1 2023
        - Integrated DataInsights for customer analytics
        - Deployed SecureConnect for PCI compliance
        
        Results:
        - 99.99% uptime achieved (up from 94%)
        - 40% reduction in infrastructure costs
        - 60% faster page load times
        - 25% increase in customer conversion rates
        
        "TechCorp's solutions have completely transformed our digital operations. 
        The migration was seamless and support has been excellent." 
        - CTO, RetailCo
        
        Timeline: 6-month implementation
        Team Size: 12 TechCorp engineers + 8 RetailCo staff
        """
    },
    {
        "name": "AI and Machine Learning Guide",
        "text": """
        Introduction to AI and Machine Learning
        
        Artificial Intelligence (AI) is the simulation of human intelligence by machines. 
        Machine Learning (ML) is a subset of AI that enables systems to learn from data.
        
        Types of Machine Learning:
        1. Supervised Learning: Training with labeled data (e.g., classification, regression)
        2. Unsupervised Learning: Finding patterns in unlabeled data (e.g., clustering)
        3. Reinforcement Learning: Learning through trial and error with rewards
        
        Common Algorithms:
        - Linear Regression: Predicting continuous values
        - Decision Trees: Classification and regression
        - Neural Networks: Deep learning for complex patterns
        - K-Means: Clustering similar data points
        
        Applications in Business:
        - Customer segmentation and personalization
        - Predictive maintenance
        - Fraud detection
        - Demand forecasting
        - Chatbots and virtual assistants
        
        Best Practices:
        - Start with clean, quality data
        - Choose the right algorithm for your problem
        - Validate models on unseen data
        - Monitor model performance over time
        - Consider ethical implications and bias
        """
    }
]

def get_sample_documents():
    """Return sample documents for testing"""
    return [
        {
            "text": doc["text"],
            "name": doc["name"],
            "type": "sample"
        }
        for doc in SAMPLE_DOCUMENTS
    ]
