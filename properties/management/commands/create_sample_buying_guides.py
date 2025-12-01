"""
Management command to create sample buying guides for the Andromeda Properties website.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from properties.models import BuyingGuide


class Command(BaseCommand):
    help = 'Creates sample buying guides for the website'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing buying guides before creating new ones',
        )

    def handle(self, *args, **options):
        if options['clear']:
            BuyingGuide.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared existing buying guides.'))

        guides_data = [
            {
                'title': 'Complete Guide for First-Time Home Buyers in Ethiopia',
                'slug': 'first-time-home-buyer-guide-ethiopia',
                'category': 'first_time_buyer',
                'excerpt': 'Everything you need to know as a first-time home buyer in Ethiopia. Learn about the buying process, legal requirements, financing options, and essential tips to make your first property purchase successful.',
                'content': '''<h2>Introduction to Home Buying in Ethiopia</h2>
<p>Buying your first home is one of the most significant financial decisions you'll make. In Ethiopia, the real estate market offers great opportunities for first-time buyers, but it's essential to understand the process and requirements.</p>

<h3>1. Understanding Your Budget</h3>
<p>Before you start looking at properties, it's crucial to determine how much you can afford:</p>
<ul>
<li>Calculate your monthly income and expenses</li>
<li>Consider down payment requirements (typically 20-30%)</li>
<li>Factor in additional costs: legal fees, taxes, insurance, and maintenance</li>
<li>Get pre-approved for a mortgage if you plan to finance</li>
</ul>

<h3>2. Finding the Right Property</h3>
<p>When searching for your first home:</p>
<ul>
<li>Consider location carefully - proximity to work, schools, and amenities</li>
<li>Think about your future needs - will the property grow with you?</li>
<li>Inspect the property thoroughly or hire a professional inspector</li>
<li>Check the property's legal status and documentation</li>
</ul>

<h3>3. Legal Requirements</h3>
<p>In Ethiopia, property transactions require:</p>
<ul>
<li>Valid property title deed</li>
<li>Property tax clearance certificate</li>
<li>Land use permit (if applicable)</li>
<li>Building permit (for constructed properties)</li>
<li>Legal verification from relevant authorities</li>
</ul>

<h3>4. Financing Options</h3>
<p>Several financing options are available:</p>
<ul>
<li>Bank mortgages - various Ethiopian banks offer home loans</li>
<li>Developer financing - some developers offer installment plans</li>
<li>Personal savings - if you have sufficient funds</li>
<li>Family loans - traditional financing method</li>
</ul>

<h3>5. The Buying Process</h3>
<ol>
<li>Property search and selection</li>
<li>Price negotiation</li>
<li>Legal verification</li>
<li>Signing the purchase agreement</li>
<li>Payment and transfer of ownership</li>
<li>Registration with relevant authorities</li>
</ol>

<h3>6. Common Mistakes to Avoid</h3>
<ul>
<li>Not conducting proper due diligence</li>
<li>Overextending your budget</li>
<li>Skipping property inspection</li>
<li>Not verifying legal documents</li>
<li>Rushing the decision</li>
</ul>

<h3>Conclusion</h3>
<p>Buying your first home in Ethiopia can be a smooth process if you're well-prepared. Take your time, do your research, and don't hesitate to seek professional advice from real estate agents, lawyers, and financial advisors.</p>''',
                'tags': 'first-time buyer, home buying, Ethiopia, real estate, property purchase, guide',
                'is_featured': True,
                'publication_date': timezone.now().date() - timedelta(days=5),
            },
            {
                'title': 'Real Estate Investment Guide: Building Wealth Through Property',
                'slug': 'real-estate-investment-guide-ethiopia',
                'category': 'investment',
                'excerpt': 'Learn how to build wealth through real estate investment in Ethiopia. Discover investment strategies, market analysis, ROI calculations, and tips for successful property investment.',
                'content': '''<h2>Real Estate Investment in Ethiopia</h2>
<p>Real estate investment has become increasingly popular in Ethiopia, offering investors opportunities for capital appreciation and rental income. This guide will help you understand the investment landscape and make informed decisions.</p>

<h3>1. Why Invest in Ethiopian Real Estate?</h3>
<ul>
<li><strong>Growing Economy:</strong> Ethiopia's economy is one of the fastest-growing in Africa</li>
<li><strong>Urbanization:</strong> Rapid urbanization creates demand for housing</li>
<li><strong>Population Growth:</strong> Young and growing population drives property demand</li>
<li><strong>Infrastructure Development:</strong> Government investments in infrastructure increase property values</li>
<li><strong>Rental Yields:</strong> Attractive rental yields in major cities like Addis Ababa</li>
</ul>

<h3>2. Types of Real Estate Investments</h3>
<h4>Residential Properties</h4>
<ul>
<li>Apartments - High demand, steady rental income</li>
<li>Houses - Long-term appreciation potential</li>
<li>Land - Development opportunities</li>
</ul>

<h4>Commercial Properties</h4>
<ul>
<li>Shops and retail spaces</li>
<li>Office buildings</li>
<li>Warehouses and storage facilities</li>
</ul>

<h3>3. Investment Strategies</h3>
<h4>Buy and Hold</h4>
<p>Purchase properties to hold long-term for rental income and appreciation.</p>

<h4>Fix and Flip</h4>
<p>Buy properties, renovate them, and sell for profit.</p>

<h4>Development</h4>
<p>Buy land and develop it into residential or commercial properties.</p>

<h3>4. Market Analysis</h3>
<p>Before investing, analyze:</p>
<ul>
<li>Location trends and growth potential</li>
<li>Property prices and rental rates</li>
<li>Supply and demand dynamics</li>
<li>Infrastructure projects planned</li>
<li>Economic indicators</li>
</ul>

<h3>5. Calculating Return on Investment (ROI)</h3>
<p>Key metrics to consider:</p>
<ul>
<li>Rental yield = (Annual rental income / Property price) × 100</li>
<li>Capital appreciation = (Current value - Purchase price) / Purchase price</li>
<li>Total ROI = Rental yield + Capital appreciation</li>
</ul>

<h3>6. Risk Management</h3>
<ul>
<li>Diversify your portfolio</li>
<li>Conduct thorough due diligence</li>
<li>Have a financial buffer for unexpected expenses</li>
<li>Stay informed about market trends</li>
<li>Work with reputable developers and agents</li>
</ul>

<h3>7. Tax Considerations</h4>
<p>Understand tax implications:</p>
<ul>
<li>Property tax</li>
<li>Capital gains tax (if applicable)</li>
<li>Rental income tax</li>
<li>Tax benefits and deductions</li>
</ul>

<h3>Conclusion</h3>
<p>Real estate investment in Ethiopia offers significant opportunities for wealth building. However, success requires careful planning, market research, and risk management. Always consult with financial advisors and real estate professionals before making investment decisions.</p>''',
                'tags': 'investment, real estate investment, property investment, ROI, wealth building, Ethiopia',
                'is_featured': True,
                'publication_date': timezone.now().date() - timedelta(days=10),
            },
            {
                'title': 'Financing Your Property Purchase: Mortgage and Loan Options',
                'slug': 'property-financing-guide-ethiopia',
                'category': 'financing',
                'excerpt': 'Comprehensive guide to financing property purchases in Ethiopia. Learn about mortgage options, loan requirements, interest rates, and how to secure the best financing for your property purchase.',
                'content': '''<h2>Financing Property Purchases in Ethiopia</h2>
<p>Most property buyers in Ethiopia require financing to complete their purchase. Understanding your financing options is crucial for making an informed decision.</p>

<h3>1. Mortgage Options in Ethiopia</h3>
<h4>Commercial Bank Mortgages</h4>
<p>Several Ethiopian banks offer mortgage products:</p>
<ul>
<li>Commercial Bank of Ethiopia (CBE)</li>
<li>Awash Bank</li>
<li>Dashen Bank</li>
<li>Bank of Abyssinia</li>
<li>Nib International Bank</li>
</ul>

<h3>2. Mortgage Requirements</h3>
<p>Typical requirements include:</p>
<ul>
<li>Proof of income (salary certificate or business income)</li>
<li>Down payment (usually 20-30% of property value)</li>
<li>Credit history check</li>
<li>Property valuation report</li>
<li>Legal documentation of the property</li>
<li>Life insurance (often required)</li>
</ul>

<h3>3. Interest Rates and Terms</h3>
<p>Mortgage terms vary by bank:</p>
<ul>
<li>Interest rates: Typically 8-12% per annum</li>
<li>Loan term: Usually 10-20 years</li>
<li>Maximum loan amount: Based on income and property value</li>
<li>Repayment: Monthly installments</li>
</ul>

<h3>4. Developer Financing</h3>
<p>Many developers offer installment plans:</p>
<ul>
<li>Lower down payment requirements</li>
<li>Flexible payment schedules</li>
<li>No bank approval needed</li>
<li>Often interest-free or low interest</li>
</ul>

<h3>5. Alternative Financing Options</h3>
<h4>Personal Loans</h4>
<p>Some banks offer personal loans for property purchase, though typically with higher interest rates.</p>

<h4>Family Financing</h4>
<p>Traditional method of borrowing from family members, often with flexible terms.</p>

<h4>Savings and Investments</h4>
<p>Using personal savings or liquidating investments to fund the purchase.</p>

<h3>6. Preparing for Mortgage Application</h3>
<ol>
<li>Check your credit score</li>
<li>Gather all required documents</li>
<li>Calculate your debt-to-income ratio</li>
<li>Save for down payment</li>
<li>Get pre-approved before house hunting</li>
</ol>

<h3>7. Comparing Loan Offers</h3>
<p>When comparing mortgage options, consider:</p>
<ul>
<li>Interest rate</li>
<li>Loan term</li>
<li>Monthly payment amount</li>
<li>Total interest paid over loan term</li>
<li>Fees and charges</li>
<li>Prepayment penalties</li>
</ul>

<h3>8. Tips for Getting Approved</h3>
<ul>
<li>Maintain a good credit history</li>
<li>Keep debt-to-income ratio below 40%</li>
<li>Have stable employment</li>
<li>Save for a substantial down payment</li>
<li>Provide complete and accurate documentation</li>
</ul>

<h3>Conclusion</h3>
<p>Securing the right financing is crucial for your property purchase. Take time to research options, compare offers, and ensure you understand all terms and conditions before committing to a loan.</p>''',
                'tags': 'financing, mortgage, loan, property finance, home loan, Ethiopia',
                'is_featured': False,
                'publication_date': timezone.now().date() - timedelta(days=15),
            },
            {
                'title': 'Legal Guide: Understanding Property Ownership and Rights in Ethiopia',
                'slug': 'property-legal-guide-ethiopia',
                'category': 'legal',
                'excerpt': 'Essential legal information about property ownership, rights, and transactions in Ethiopia. Learn about title deeds, property registration, legal requirements, and protecting your property rights.',
                'content': '''<h2>Property Law in Ethiopia</h2>
<p>Understanding property law is essential for any property buyer or owner in Ethiopia. This guide covers key legal aspects of property ownership and transactions.</p>

<h3>1. Types of Property Ownership</h3>
<h4>Private Ownership</h4>
<p>Private individuals and entities can own property in Ethiopia, subject to certain restrictions.</p>

<h4>Leasehold</h4>
<p>Properties can be held on lease from the government or private owners, typically for 99 years.</p>

<h3>2. Title Deeds and Documentation</h3>
<p>Essential documents for property ownership:</p>
<ul>
<li><strong>Title Deed:</strong> Primary document proving ownership</li>
<li><strong>Land Use Permit:</strong> Required for land development</li>
<li><strong>Building Permit:</strong> Required for construction</li>
<li><strong>Property Tax Clearance:</strong> Proof of tax compliance</li>
<li><strong>Survey Certificate:</strong> Defines property boundaries</li>
</ul>

<h3>3. Property Registration</h3>
<p>All property transactions must be registered with:</p>
<ul>
<li>Ministry of Urban Development and Construction</li>
<li>Regional Land Administration Offices</li>
<li>Municipal authorities</li>
</ul>

<h3>4. Due Diligence Process</h3>
<p>Before purchasing, verify:</p>
<ol>
<li>Property title is clear and valid</li>
<li>No liens or encumbrances</li>
<li>Property boundaries are accurate</li>
<li>All taxes are paid</li>
<li>No legal disputes</li>
<li>Seller has legal right to sell</li>
</ol>

<h3>5. Purchase Agreement</h3>
<p>A proper purchase agreement should include:</p>
<ul>
<li>Property description and location</li>
<li>Purchase price and payment terms</li>
<li>Transfer date</li>
<li>Conditions and warranties</li>
<li>Dispute resolution mechanisms</li>
</ul>

<h3>6. Property Rights and Restrictions</h3>
<h4>Rights of Property Owners</h4>
<ul>
<li>Right to use and enjoy the property</li>
<li>Right to sell or transfer</li>
<li>Right to lease or rent</li>
<li>Right to develop (with permits)</li>
</ul>

<h4>Common Restrictions</h4>
<ul>
<li>Zoning regulations</li>
<li>Building height restrictions</li>
<li>Environmental regulations</li>
<li>Heritage site protections</li>
</ul>

<h3>7. Property Taxes</h3>
<p>Property owners are responsible for:</p>
<ul>
<li>Annual property tax</li>
<li>Capital gains tax (on sale)</li>
<li>Transfer tax (on purchase)</li>
<li>Stamp duty</li>
</ul>

<h3>8. Dispute Resolution</h3>
<p>If disputes arise:</p>
<ul>
<li>Mediation through local authorities</li>
<li>Court proceedings</li>
<li>Arbitration (if agreed in contract)</li>
</ul>

<h3>9. Working with Legal Professionals</h3>
<p>It's highly recommended to:</p>
<ul>
<li>Hire a qualified lawyer for property transactions</li>
<li>Conduct legal verification before purchase</li>
<li>Review all documents carefully</li>
<li>Get legal advice on complex transactions</li>
</ul>

<h3>Conclusion</h3>
<p>Understanding property law protects your investment and ensures smooth transactions. Always conduct proper due diligence and work with qualified legal professionals when buying or selling property in Ethiopia.</p>''',
                'tags': 'legal, property law, title deed, property rights, Ethiopia, real estate law',
                'is_featured': False,
                'publication_date': timezone.now().date() - timedelta(days=20),
            },
            {
                'title': '10 Essential Tips for Buying Property in Addis Ababa',
                'slug': 'tips-buying-property-addis-ababa',
                'category': 'tips',
                'excerpt': 'Practical tips and advice for buying property in Addis Ababa. Learn from experts about location selection, negotiation strategies, property inspection, and common pitfalls to avoid.',
                'content': '''<h2>Tips for Buying Property in Addis Ababa</h2>
<p>Addis Ababa's real estate market is dynamic and growing. Here are essential tips to help you make the right property purchase decision.</p>

<h3>1. Research the Location Thoroughly</h3>
<p>Location is crucial in real estate:</p>
<ul>
<li>Check proximity to your workplace</li>
<li>Evaluate access to schools, hospitals, and shopping</li>
<li>Consider future development plans in the area</li>
<li>Check transportation links and traffic patterns</li>
<li>Research neighborhood safety and security</li>
</ul>

<h3>2. Work with Reputable Real Estate Agents</h3>
<p>A good agent can:</p>
<ul>
<li>Save you time in property search</li>
<li>Provide market insights and pricing guidance</li>
<li>Help with negotiations</li>
<li>Assist with legal and administrative processes</li>
<li>Connect you with trusted professionals</li>
</ul>

<h3>3. Verify Property Documentation</h3>
<p>Never skip document verification:</p>
<ul>
<li>Check title deed authenticity</li>
<li>Verify property boundaries</li>
<li>Confirm no outstanding taxes or liens</li>
<li>Ensure seller has legal right to sell</li>
<li>Get professional legal verification</li>
</ul>

<h3>4. Inspect the Property Carefully</h3>
<p>Thorough inspection helps avoid costly surprises:</p>
<ul>
<li>Check structural integrity</li>
<li>Inspect plumbing and electrical systems</li>
<li>Look for water damage or leaks</li>
<li>Check for pest infestations</li>
<li>Evaluate overall condition</li>
<li>Consider hiring a professional inspector</li>
</ul>

<h3>5. Understand the True Cost</h3>
<p>Beyond the purchase price, consider:</p>
<ul>
<li>Legal fees and registration costs</li>
<li>Property taxes</li>
<li>Maintenance and repair costs</li>
<li>Utilities and service charges</li>
<li>Insurance premiums</li>
<li>Future renovation needs</li>
</ul>

<h3>6. Negotiate Effectively</h3>
<p>Good negotiation can save you money:</p>
<ul>
<li>Research comparable property prices</li>
<li>Understand market conditions</li>
<li>Identify property issues for leverage</li>
<li>Be prepared to walk away</li>
<li>Consider timing (end of month/quarter)</li>
</ul>

<h3>7. Check Infrastructure and Amenities</h3>
<p>Evaluate available infrastructure:</p>
<ul>
<li>Road access and quality</li>
<li>Water and electricity supply</li>
<li>Internet and telecommunications</li>
<li>Waste management</li>
<li>Security services</li>
<li>Recreational facilities</li>
</ul>

<h3>8. Consider Future Value</h3>
<p>Think long-term:</p>
<ul>
<li>Research area development plans</li>
<li>Consider property appreciation potential</li>
<li>Evaluate rental income potential</li>
<li>Assess resale value</li>
</ul>

<h3>9. Get Everything in Writing</h3>
<p>Document all agreements:</p>
<ul>
<li>Purchase price and payment terms</li>
<li>Included items and fixtures</li>
<li>Repairs or improvements promised</li>
<li>Timeline for completion</li>
<li>Contingencies and conditions</li>
</ul>

<h3>10. Don't Rush the Decision</h3>
<p>Take your time:</p>
<ul>
<li>View multiple properties</li>
<li>Compare options carefully</li>
<li>Sleep on major decisions</li>
<li>Consult with family and advisors</li>
<li>Trust your instincts</li>
</ul>

<h3>Common Mistakes to Avoid</h3>
<ul>
<li>Buying without proper inspection</li>
<li>Skipping legal verification</li>
<li>Overextending your budget</li>
<li>Ignoring location factors</li>
<li>Not reading contracts carefully</li>
<li>Rushing due to pressure</li>
</ul>

<h3>Conclusion</h3>
<p>Buying property in Addis Ababa requires careful planning and research. Follow these tips, work with professionals, and take your time to make the right decision. Your property purchase is a significant investment - make it count!</p>''',
                'tags': 'tips, advice, Addis Ababa, property buying, real estate tips, Ethiopia',
                'is_featured': True,
                'publication_date': timezone.now().date() - timedelta(days=3),
            },
            {
                'title': 'Understanding Property Prices and Market Trends in Ethiopia',
                'slug': 'property-prices-market-trends-ethiopia',
                'category': 'tips',
                'excerpt': 'Learn about property pricing in Ethiopia, market trends, factors affecting prices, and how to determine fair market value when buying or selling property.',
                'content': '''<h2>Property Prices and Market Trends in Ethiopia</h2>
<p>Understanding property prices and market dynamics is essential for making informed real estate decisions in Ethiopia.</p>

<h3>1. Factors Affecting Property Prices</h3>
<h4>Location</h4>
<p>Location is the primary price determinant:</p>
<ul>
<li>Prime areas command higher prices</li>
<li>Proximity to city center</li>
<li>Access to amenities and services</li>
<li>Neighborhood reputation</li>
</ul>

<h4>Property Type and Size</h4>
<ul>
<li>Larger properties generally cost more</li>
<li>Apartments vs. houses</li>
<li>Commercial vs. residential</li>
<li>Number of bedrooms and bathrooms</li>
</ul>

<h4>Property Condition</h4>
<ul>
<li>New vs. old properties</li>
<li>Renovation status</li>
<li>Quality of construction</li>
<li>Maintenance history</li>
</ul>

<h4>Infrastructure and Amenities</h4>
<ul>
<li>Road access</li>
<li>Utilities availability</li>
<li>Security services</li>
<li>Recreational facilities</li>
</ul>

<h3>2. Market Trends in Ethiopia</h3>
<h4>Growing Demand</h4>
<p>Several factors drive demand:</p>
<ul>
<li>Rapid urbanization</li>
<li>Growing middle class</li>
<li>Population growth</li>
<li>Economic development</li>
</ul>

<h4>Price Trends</h4>
<p>Property prices have generally trended upward, though with regional variations:</p>
<ul>
<li>Addis Ababa: Strong growth in prime areas</li>
<li>Secondary cities: Moderate growth</li>
<li>New developments: Competitive pricing</li>
</ul>

<h3>3. Determining Fair Market Value</h3>
<p>Methods to assess property value:</p>
<ul>
<li><strong>Comparative Market Analysis:</strong> Compare with similar properties</li>
<li><strong>Professional Appraisal:</strong> Get expert valuation</li>
<li><strong>Cost Approach:</strong> Land value + construction cost</li>
<li><strong>Income Approach:</strong> For rental properties</li>
</ul>

<h3>4. Price Ranges by Property Type</h3>
<h4>Apartments</h4>
<ul>
<li>Studio/1-bedroom: Varies by location</li>
<li>2-bedroom: Moderate pricing</li>
<li>3+ bedroom: Premium pricing</li>
</ul>

<h4>Houses</h4>
<ul>
<li>Villa-style: Premium pricing</li>
<li>Standard houses: Mid-range</li>
<li>Older houses: Lower pricing</li>
</ul>

<h3>5. Negotiation Strategies</h3>
<p>When negotiating price:</p>
<ul>
<li>Research comparable sales</li>
<li>Identify property issues</li>
<li>Consider market conditions</li>
<li>Be prepared with data</li>
<li>Know your maximum budget</li>
</ul>

<h3>6. Future Price Considerations</h3>
<p>Factors that may affect future prices:</p>
<ul>
<li>Infrastructure development</li>
<li>Economic growth</li>
<li>Government policies</li>
<li>Supply and demand balance</li>
<li>Interest rates</li>
</ul>

<h3>Conclusion</h3>
<p>Understanding property prices and market trends helps you make informed decisions. Always research thoroughly, get professional advice, and consider both current value and future potential when buying or selling property.</p>''',
                'tags': 'property prices, market trends, real estate market, Ethiopia, property valuation',
                'is_featured': False,
                'publication_date': timezone.now().date() - timedelta(days=7),
            },
        ]

        created_count = 0
        for guide_data in guides_data:
            guide, created = BuyingGuide.objects.get_or_create(
                slug=guide_data['slug'],
                defaults={
                    'title': guide_data['title'],
                    'category': guide_data['category'],
                    'excerpt': guide_data['excerpt'],
                    'content': guide_data['content'],
                    'tags': guide_data['tags'],
                    'is_published': True,
                    'is_featured': guide_data['is_featured'],
                    'publication_date': guide_data['publication_date'],
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created: {guide.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Skipped (already exists): {guide.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created {created_count} buying guide(s).'
            )
        )

