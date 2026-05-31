"""
Skill Extractor Module - Identifies technical and professional skills from text
Uses multiple methods: direct matching, fuzzy matching, and semantic matching
"""

from typing import List, Dict, Set
import re
from fuzzywuzzy import fuzz
from collections import defaultdict


class SkillExtractor:
    """Extract skills from resume and job description text"""
    
    # Master skills database (500+ skills across all industries)
    MASTER_SKILLS = {
        # ===== PROGRAMMING LANGUAGES =====
        'python', 'java', 'javascript', 'typescript', 'cpp', 'c#', 'c', 'c++', 'php',
        'ruby', 'go', 'rust', 'kotlin', 'swift', 'objective-c', 'scala', 'r',
        'matlab', 'groovy', 'perl', 'lua', 'shell', 'bash', 'powershell', 'vb.net',
        'delphi', 'haskell', 'erlang', 'elixir', 'clojure', 'lisp', 'scheme',
        'f#', 'ocaml', 'julia', 'dart', 'kotlin', 'crystal', 'nim',
        'verilog', 'vhdl', 'assembly', 'cobol', 'fortran', 'ada',
        
        # ===== WEB FRAMEWORKS & FRONTEND =====
        'html', 'html5', 'css', 'css3', 'sass', 'less', 'postcss',
        'react', 'react.js', 'vue', 'vue.js', 'angular', 'angular.js',
        'node.js', 'express', 'express.js', 'next.js', 'gatsby', 'nuxt', 'svelte',
        'jquery', 'bootstrap', 'tailwind', 'material ui', 'ant design',
        'django', 'flask', 'fastapi', 'pyramid', 'tornado',
        'spring', 'spring boot', 'spring mvc', 'hibernate', 'jpa', 'ejb',
        'asp.net', 'asp.net core', '.net', 'blazor', 'mvc',
        'laravel', 'symfony', 'yii', 'zend', 'slim', 'lumen',
        'ruby on rails', 'sinatra', 'hanami', 'grape',
        'graphql', 'rest api', 'restful', 'soap', 'json', 'xml',
        'webpack', 'gulp', 'grunt', 'parcel', 'vite', 'rollup',
        'npm', 'yarn', 'pnpm', 'bun', 'pip', 'conda',
        'eslint', 'prettier', 'prettier', 'typescript', 'babel',
        'redux', 'vuex', 'zustand', 'context api', 'mobx', 'recoil',
        
        # ===== DATABASES & DATA STORAGE =====
        'sql', 'mysql', 'postgresql', 'postgres', 'mongodb', 'redis',
        'cassandra', 'elasticsearch', 'dynamodb', 'firebase', 'firestore',
        'oracle', 'sql server', 'mariadb', 'sqlite', 'h2',
        'couchdb', 'neo4j', 'influxdb', 'timescaledb', 'prometheus',
        'memcached', 'etcd', 'consul', 'vault', 'zookeeper',
        'bigquery', 'redshift', 'snowflake', 'athena', 'presto',
        'druid', 'clickhouse', 'vertica', 'greenplum', 'exasol',
        'arangodb', 'mongodb', 'couchbase', 'rethinkdb', 'voltdb',
        'database design', 'data modeling', 'sql tuning', 'query optimization',
        
        # ===== CLOUD PLATFORMS =====
        'aws', 'amazon aws', 'azure', 'gcp', 'google cloud', 'google cloud platform',
        'ec2', 's3', 'rds', 'lambda', 'sqs', 'sns', 'kinesis',
        'app engine', 'cloud functions', 'cloud run', 'bigquery', 'datastore',
        'app service', 'azure sql', 'azure storage', 'azure functions', 'cosmos db',
        'docker', 'docker compose', 'kubernetes', 'k8s', 'helm',
        'openshift', 'cloud foundry', 'nomad', 'mesos', 'swarm',
        'heroku', 'digitalocean', 'linode', 'vultr', 'aws lightsail',
        'openstack', 'eucalyptus', 'cloudstack', 'privatev cloud',
        
        # ===== DEVOPS & CI/CD =====
        'ci/cd', 'continuous integration', 'continuous deployment', 'continuous delivery',
        'jenkins', 'gitlab ci', 'github actions', 'circleci', 'travis ci',
        'travis', 'appveyor', 'buildkite', 'drone', 'teamcity', 'bamboo',
        'gitlab', 'github', 'bitbucket', 'gitea', 'gitlab', 'gogs',
        'git', 'svn', 'mercurial', 'perforce', 'version control',
        'terraform', 'terraform hcl', 'ansible', 'puppet', 'chef', 'salt',
        'cloudformation', 'arm templates', 'iac', 'infrastructure as code',
        'serverless', 'serverless framework', 'sam', 'chalice',
        'container orchestration', 'container registry', 'ecr', 'gcr', 'acr',
        'monitoring', 'prometheus', 'grafana', 'datadog', 'newrelic', 'splunk',
        'elk stack', 'elasticsearch', 'logstash', 'kibana', 'fluentd', 'filebeat',
        'observability', 'logging', 'metrics', 'tracing', 'opentelemetry',
        'jaeger', 'zipkin', 'apm', 'application performance monitoring',
        
        # ===== DATA SCIENCE & ML =====
        'data science', 'machine learning', 'deep learning', 'neural networks',
        'tensorflow', 'keras', 'pytorch', 'scikit-learn', 'sklearn',
        'xgboost', 'lightgbm', 'catboost', 'gradient boosting',
        'computer vision', 'natural language processing', 'nlp', 'nlp models',
        'cv', 'image processing', 'object detection', 'yolo', 'rcnn',
        'nlp', 'transformers', 'bert', 'gpt', 'gpt2', 'gpt3', 'llm', 'large language model',
        'huggingface', 'langchain', 'llama', 'mistral', 'claude', 'openai',
        'supervised learning', 'unsupervised learning', 'reinforcement learning',
        'regression', 'classification', 'clustering', 'dimensionality reduction',
        'pca', 'tsne', 'kmeans', 'hierarchical clustering', 'dbscan',
        'pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn', 'plotly',
        'jupyter', 'notebook', 'colab', 'kaggle', 'databricks',
        'feature engineering', 'feature extraction', 'feature selection',
        'model training', 'model evaluation', 'cross validation', 'hyperparameter tuning',
        'overfitting', 'underfitting', 'regularization', 'loss functions',
        'optimization', 'sgd', 'adam', 'rmsprop', 'momentum', 'gradient descent',
        'ensemble methods', 'bagging', 'boosting', 'stacking', 'voting',
        'time series', 'arima', 'lstm', 'rnn', 'gru', 'attention mechanisms',
        'data analysis', 'statistical analysis', 'hypothesis testing',
        'descriptive statistics', 'inferential statistics', 'experimental design',
        'data visualization', 'tableau', 'power bi', 'looker', 'qlik',
        'apache spark', 'pyspark', 'hadoop', 'hive', 'pig', 'hbase',
        'mapreduce', 'distributed computing', 'spark streaming', 'kafka',
        
        # ===== TESTING & QA =====
        'unit testing', 'integration testing', 'e2e testing', 'end to end testing',
        'system testing', 'acceptance testing', 'performance testing', 'load testing',
        'stress testing', 'penetration testing', 'security testing', 'usability testing',
        'test automation', 'automated testing', 'test framework', 'test suite',
        'selenium', 'webdriver', 'cypress', 'playwrightio', 'playwright',
        'puppeteer', 'nightwatch', 'protractor', 'testcafe', 'phantom',
        'junit', 'testng', 'pytest', 'nunit', 'xunit', 'mocha', 'jasmine',
        'jest', 'vitest', 'chai', 'assert', 'mock', 'stub', 'spy',
        'unittest', 'doctest', 'hypothesis', 'property based testing',
        'cucumber', 'behave', 'specflow', 'gherkin', 'bdd', 'tdd',
        'appium', 'xctest', 'espresso', 'uiautomator', 'robolectric',
        'postman', 'insomnia', 'restclient', 'soapui', 'jmeter', 'gatling',
        'loadrunner', 'neoload', 'k6', 'locust', 'artillery',
        'bug tracking', 'issue tracking', 'jira', 'bugzilla', 'redmine', 'youtrack',
        'testcase management', 'test plan', 'test execution', 'coverage analysis',
        'code coverage', 'jacoco', 'coverage.py', 'nyc', 'istanbul',
        'qa', 'quality assurance', 'quality control', 'continuous testing',
        
        # ===== MOBILE DEVELOPMENT =====
        'ios', 'iphone', 'ipad', 'swift', 'objective-c', 'cocoa', 'cocoapods',
        'android', 'kotlin', 'java', 'android studio', 'gradle', 'aac',
        'react native', 'flutter', 'dart', 'xamarin', 'c#', 'cordova',
        'ionic', 'phonegap', 'nativescript', 'capacitor', 'expo',
        'mobile development', 'mobile app', 'app development', 'cross platform',
        'native development', 'hybrid development', 'progressive web app', 'pwa',
        'firebase', 'google play services', 'apple app store', 'app distribution',
        'ui design', 'ux design', 'user experience', 'user interface',
        'accessibility', 'a11y', 'wcag', 'aria', 'usability',
        
        # ===== GAME DEVELOPMENT =====
        'game development', 'game engine', 'unity', 'unreal engine', 'godot',
        'c#', 'c++', 'unity3d', 'unreal', 'cocos2d',
        'graphics programming', 'directx', 'opengl', 'vulkan', 'metal',
        'physics engine', 'bullet', 'havok', 'physx', 'chipmunk',
        'game design', 'level design', 'character design', 'animation',
        'sound design', 'game audio', 'wwise', 'fmod', 'audiokinetic',
        'multiplayer', 'networking', 'netcode', 'networking programming',
        'vr', 'ar', 'virtual reality', 'augmented reality', 'mixed reality',
        'steam', 'epic games', 'playstation', 'xbox', 'nintendo',
        
        # ===== DESIGN & UX =====
        'graphic design', 'ui design', 'ux design', 'web design',
        'design thinking', 'user research', 'wireframing', 'prototyping',
        'interaction design', 'information architecture', 'user testing',
        'adobe xd', 'figma', 'sketch', 'invision', 'framer', 'protopie',
        'photoshop', 'illustrator', 'indesign', 'lightroom', 'premiere',
        'after effects', 'blender', '3d modeling', '3d design', 'cad',
        'autocad', 'solidworks', 'fusion 360', 'revit', '3ds max',
        'maya', 'cinema 4d', 'zbrush', 'substance painter', 'unity',
        'accessibility', 'responsive design', 'mobile first', 'progressive enhancement',
        'color theory', 'typography', 'layout', 'composition', 'branding',
        
        # ===== PROJECT MANAGEMENT =====
        'project management', 'agile', 'scrum', 'kanban', 'waterfall',
        'agile methodology', 'scrum master', 'product owner', 'sprint',
        'lean', 'six sigma', 'lean six sigma', 'agile leadership',
        'risk management', 'scope management', 'time management',
        'resource management', 'stakeholder management', 'communication',
        'jira', 'asana', 'monday.com', 'trello', 'notion',
        'microsoft project', 'smartsheet', 'wrike', 'teamwork',
        'confluence', 'slack', 'microsoft teams', 'zoom', 'google workspace',
        'confluence', 'documentation', 'knowledge management',
        
        # ===== BUSINESS & SOFT SKILLS =====
        'communication', 'public speaking', 'presentation', 'storytelling',
        'leadership', 'management', 'team leadership', 'people management',
        'conflict resolution', 'negotiation', 'decision making',
        'critical thinking', 'problem solving', 'creative thinking',
        'analytical thinking', 'strategic thinking', 'systems thinking',
        'collaboration', 'teamwork', 'cooperation', 'partnership',
        'time management', 'organization', 'planning', 'prioritization',
        'adaptability', 'flexibility', 'resilience', 'stress management',
        'emotional intelligence', 'empathy', 'self awareness',
        'motivation', 'initiative', 'accountability', 'responsibility',
        'customer service', 'customer focus', 'customer satisfaction',
        'sales', 'business development', 'account management',
        'negotiation', 'relationship building', 'networking',
        'business strategy', 'business analysis', 'competitive analysis',
        'market research', 'competitive intelligence', 'industry analysis',
        'financial analysis', 'roi', 'roi analysis', 'budgeting',
        'business writing', 'technical writing', 'copywriting', 'content writing',
        
        # ===== FINANCE & ACCOUNTING =====
        'accounting', 'financial accounting', 'managerial accounting',
        'gaap', 'ifrs', 'audit', 'internal audit', 'external audit',
        'tax accounting', 'tax planning', 'tax compliance',
        'financial reporting', 'financial analysis', 'financial forecasting',
        'budgeting', 'cost analysis', 'variance analysis', 'forecasting',
        'general ledger', 'accounts payable', 'accounts receivable',
        'payroll', 'payroll processing', 'benefits administration',
        'quickbooks', 'sap', 'oracle financials', 'salesforce', 'workday',
        'excel', 'advanced excel', 'pivot tables', 'vlookup', 'macros', 'vba',
        'power query', 'power pivot', 'power bi', 'tableau', 'analytics',
        'investments', 'portfolio management', 'risk management',
        'financial planning', 'financial modeling', 'valuation',
        'mergers and acquisitions', 'm&a', 'ipo', 'private equity',
        
        # ===== MARKETING & SALES =====
        'digital marketing', 'marketing', 'content marketing', 'email marketing',
        'social media marketing', 'seo', 'search engine optimization',
        'sem', 'search engine marketing', 'ppc', 'pay per click',
        'google ads', 'facebook ads', 'linkedin ads', 'twitter ads',
        'marketing automation', 'hubspot', 'marketo', 'salesforce',
        'crm', 'customer relationship management', 'salesforce crm',
        'brand management', 'brand strategy', 'brand development',
        'product management', 'product marketing', 'product development',
        'market research', 'consumer insights', 'competitive analysis',
        'sales', 'sales strategy', 'sales management', 'account management',
        'business development', 'bd', 'lead generation', 'lead nurturing',
        'sales operations', 'sales enablement', 'sales analytics',
        'pricing strategy', 'promotional strategy', 'customer retention',
        'customer acquisition', 'customer lifetime value', 'clv',
        
        # ===== HUMAN RESOURCES =====
        'human resources', 'hr', 'recruitment', 'talent acquisition',
        'talent management', 'talent development', 'employee engagement',
        'onboarding', 'offboarding', 'performance management',
        'compensation', 'benefits', 'rewards', 'recognition',
        'training', 'learning and development', 'l&d', 'instructional design',
        'organizational development', 'change management', 'organizational culture',
        'diversity and inclusion', 'di', 'equity', 'belonging',
        'employee relations', 'employee wellbeing', 'mental health',
        'labor relations', 'compliance', 'employment law',
        'hr analytics', 'people analytics', 'predictive analytics',
        'workday', 'successfactors', 'bamboohr', 'zenefits',
        
        # ===== HEALTHCARE & MEDICAL =====
        'healthcare', 'medical', 'nursing', 'patient care',
        'clinical care', 'diagnosis', 'treatment', 'therapy',
        'medical coding', 'billing', 'claims', 'insurance',
        'emr', 'ehr', 'electronic health records', 'hipaa',
        'healthcare it', 'clinical informatics', 'health informatics',
        'pharmacy', 'pharmacology', 'pharmaceutical',
        'telemedicine', 'telehealth', 'remote healthcare',
        'public health', 'epidemiology', 'disease control',
        'medical research', 'clinical research', 'trials', 'fda',
        'medical device', 'medical equipment', 'surgical instruments',
        'anesthesia', 'radiology', 'pathology', 'laboratory',
        'cardiology', 'oncology', 'neurology', 'orthopedics',
        'surgery', 'internal medicine', 'pediatrics', 'psychiatry',
        'dentistry', 'optometry', 'dermatology', 'rheumatology',
        'immunology', 'gastroenterology', 'urology', 'nephrology',
        'pulmonology', 'endocrinology', 'hematology', 'infectious disease',
        
        # ===== LEGAL & COMPLIANCE =====
        'legal', 'law', 'contract law', 'corporate law', 'employment law',
        'intellectual property', 'ip', 'patents', 'trademarks', 'copyrights',
        'litigation', 'compliance', 'regulatory compliance', 'audit',
        'gdpr', 'ccpa', 'hipaa', 'sox', 'pci dss', 'iso',
        'legal documentation', 'contract drafting', 'legal writing',
        'paralegal', 'legal research', 'legal analysis',
        'corporate governance', 'risk management', 'regulatory affairs',
        'contract management', 'vendor management', 'supplier management',
        'mergers and acquisitions', 'ip management', 'litigation support',
        
        # ===== EDUCATION =====
        'teaching', 'education', 'instructional design', 'curriculum design',
        'learning management', 'lms', 'moodle', 'canvas', 'blackboard',
        'online learning', 'e learning', 'distance learning',
        'tutoring', 'mentoring', 'coaching', 'training',
        'student assessment', 'grading', 'academic advising',
        'educational technology', 'edtech', 'learning technology',
        'classroom management', 'student engagement', 'student retention',
        'special education', 'ell', 'english language learner',
        'stem', 'steam', 'critical thinking', 'problem solving',
        
        # ===== MANUFACTURING & OPERATIONS =====
        'manufacturing', 'operations', 'supply chain', 'logistics',
        'inventory management', 'warehouse management', 'wms',
        'production planning', 'production control', 'quality control',
        'lean manufacturing', 'six sigma', 'kaizen', 'continuous improvement',
        'equipment maintenance', 'preventive maintenance', 'predictive maintenance',
        'safety', 'industrial hygiene', 'ergonomics', 'osha',
        'procurement', 'purchasing', 'vendor management', 'supplier management',
        'distribution', 'fulfillment', 'order management',
        'manufacturing execution', 'mes', 'erp', 'enterprise resource planning',
        'sap', 'oracle', 'netsuite', 'epicor', 'infor',
        'robotics', 'automation', 'iot', 'sensors', 'real time monitoring',
        
        # ===== RETAIL & E-COMMERCE =====
        'retail', 'e commerce', 'ecommerce', 'merchandising',
        'store management', 'inventory management', 'pos', 'point of sale',
        'customer service', 'customer experience', 'cx',
        'pricing', 'promotion', 'sales', 'revenue management',
        'supply chain', 'logistics', 'fulfillment', 'warehousing',
        'shopify', 'woocommerce', 'magento', 'bigcommerce', 'prestashop',
        'amazon', 'ebay', 'alibaba', 'marketplace management',
        'product catalog', 'product information management', 'pim',
        'payment processing', 'fraud detection', 'risk management',
        'analytics', 'reporting', 'business intelligence', 'bi',
        
        # ===== REAL ESTATE & CONSTRUCTION =====
        'real estate', 'property management', 'facilities management',
        'construction', 'project management', 'site management',
        'building information modeling', 'bim', 'cad', 'autocad',
        'architectural design', 'landscape design', 'interior design',
        'estimating', 'cost analysis', 'budgeting',
        'zoning', 'permits', 'code compliance', 'safety',
        'residential', 'commercial', 'industrial', 'retail',
        'valuation', 'appraisal', 'market analysis', 'investment analysis',
        'leasing', 'tenant management', 'maintenance', 'repairs',
        'sustainability', 'green building', 'leed', 'energy efficiency',
        
        # ===== TELECOMMUNICATIONS & NETWORKING =====
        'networking', 'network administration', 'network engineering',
        'routers', 'switches', 'firewalls', 'vpn', 'wan', 'lan',
        'tcp/ip', 'dns', 'dhcp', 'nat', 'bgp', 'ospf', 'eigrp',
        'cisco', 'juniper', 'arista', 'fortinet', 'checkpoint',
        'network security', 'intrusion detection', 'ids', 'ips',
        'web application firewall', 'waf', 'ddos', 'mitigation',
        'telecommunications', 'voip', 'sip', 'pbx', 'call center',
        '5g', '4g', 'lte', 'wireless', 'wifi', '802.11',
        'mobile networks', 'carrier', 'broadband', 'internet service provider',
        
        # ===== SECURITY =====
        'cybersecurity', 'security', 'information security', 'infosec',
        'network security', 'application security', 'appsec',
        'cloud security', 'data security', 'database security',
        'encryption', 'cryptography', 'ssl', 'tls', 'certificates',
        'authentication', 'authorization', 'access control', 'iam',
        'multi factor authentication', 'mfa', 'two factor', '2fa',
        'sso', 'oauth', 'saml', 'ldap', 'kerberos',
        'vulnerability management', 'penetration testing', 'pentest',
        'web application security', 'owasp', 'burp suite', 'zaproxy',
        'incident response', 'forensics', 'malware analysis',
        'threat intelligence', 'threat hunting', 'siem',
        'security operations', 'soc', 'security monitoring',
        'compliance', 'audit', 'risk management', 'governance',
        'privacy', 'data protection', 'gdpr', 'ccpa', 'pii',
        
        # ===== ENVIRONMENTAL & SUSTAINABILITY =====
        'sustainability', 'environmental', 'green', 'carbon',
        'renewable energy', 'solar', 'wind', 'hydroelectric',
        'energy management', 'energy efficiency', 'conservation',
        'waste management', 'recycling', 'circular economy',
        'environmental compliance', 'epa', 'environmental law',
        'environmental science', 'ecology', 'conservation',
        'climate change', 'climate science', 'climate policy',
        'leed', 'green building', 'sustainable design',
        'corporate social responsibility', 'csr', 'esg', 'impact',
        
        # ===== OTHER TECHNICAL SKILLS =====
        'linux', 'ubuntu', 'centos', 'rhel', 'debian', 'unix',
        'windows server', 'active directory', 'group policy',
        'macos', 'ios', 'android',
        'virtualization', 'vmware', 'hyper-v', 'kvm', 'xen',
        'storage', 'nas', 'san', 'backup', 'disaster recovery',
        'high availability', 'ha', 'clustering', 'load balancing',
        'database administration', 'dba', 'backup', 'recovery', 'replication',
        'system administration', 'sysadmin', 'server administration',
        'scripting', 'automation', 'shell scripting', 'python scripting',
        'api', 'api design', 'api development', 'rest', 'soap', 'graphql',
        'microservices', 'microservices architecture', 'distributed systems',
        'service oriented architecture', 'soa', 'enterprise architecture',
        'event driven architecture', 'event streaming', 'kafka',
        'message queue', 'amq', 'rabbitmq', 'activemq',
        'api gateway', 'api management', 'kong', 'apigee',
        'service mesh', 'istio', 'linkerd', 'consul',
        'container', 'containerization', 'docker', 'podman',
        'container registry', 'docker registry', 'harbor', 'quay',
        'container orchestration', 'kubernetes', 'openshift', 'ecs',
        'serverless', 'functions as a service', 'faas', 'lambda',
        'edge computing', 'fog computing', 'iot',
        'blockchain', 'cryptocurrency', 'ethereum', 'smart contracts',
        'web3', 'defi', 'nft', 'distributed ledger',
        'quantum computing', 'quantum algorithms',
        'ai', 'artificial intelligence', 'machine learning', 'deep learning',
        'nlp', 'computer vision', 'robotics', 'automation',
        'augmented reality', 'ar', 'virtual reality', 'vr',
        'extended reality', 'xr', 'mixed reality', 'mr',
        'internet of things', 'iot', 'sensors', 'embedded systems',
        'firmware', 'device drivers', 'kernel', 'os development',
        'performance optimization', 'load testing', 'stress testing',
        'capacity planning', 'resource planning', 'scaling',
    }
    
    def __init__(self, fuzzy_threshold: int = 70):
        """Initialize skill extractor with improved threshold
        
        Args:
            fuzzy_threshold: Minimum similarity score (0-100) for fuzzy matching - lowered to 70 for better detection
        """
        self.fuzzy_threshold = fuzzy_threshold
        self.extracted_skills: List[Dict] = []
    
    def extract(self, text: str) -> List[str]:
        """Extract skills from text - returns list of skill names
        
        Args:
            text: Text to extract skills from
            
        Returns:
            List of skill names found
        """
        try:
            result = self.extract_skills(text)
            return [item['skill'] for item in result]
        except Exception:
            return []
    
    def extract_skills(self, text: str, job_text: str = None) -> List[Dict]:
        """
        Extract skills from text using multiple methods
        
        Args:
            text: Resume or job description text
            job_text: Optional job description for context
            
        Returns:
            List of dicts with keys: skill, confidence (0-1), method, occurrences
        """
        # Validate input
        if not text or not isinstance(text, str) or len(text.strip()) == 0:
            return []
        
        # Convert to lowercase for matching
        text_lower = text.lower()
        
        # Track extracted skills to avoid duplicates
        skills_dict = {}
        
        # Method 1: Direct matching (60% confidence)
        for skill in self.MASTER_SKILLS:
            mentions = self._find_skill_mentions(skill, text_lower)
            if mentions > 0:
                skills_dict[skill] = {
                    'skill': skill,
                    'confidence': 0.6,
                    'method': 'direct',
                    'occurrences': mentions
                }
        
        # Method 2: Fuzzy matching for variations (80%+ confidence)
        fuzzy_skills = self._fuzzy_match_skills(text_lower)
        for skill, info in fuzzy_skills.items():
            if skill not in skills_dict:
                skills_dict[skill] = {
                    'skill': skill,
                    'confidence': min(info['score'] / 100.0, 0.95),
                    'method': 'fuzzy',
                    'occurrences': info['occurrences']
                }
        
        # Method 3: Semantic matching with keywords (70% confidence)
        semantic_skills = self._semantic_match_skills(text_lower)
        for skill in semantic_skills:
            if skill not in skills_dict:
                mentions = self._find_skill_mentions(skill, text_lower)
                skills_dict[skill] = {
                    'skill': skill,
                    'confidence': 0.7,
                    'method': 'semantic',
                    'occurrences': mentions
                }
        
        # Sort by confidence and occurrences
        result = sorted(
            skills_dict.values(),
            key=lambda x: (x['confidence'], x['occurrences']),
            reverse=True
        )
        
        self.extracted_skills = result
        return result
    
    def _find_skill_mentions(self, skill: str, text: str) -> int:
        """Count mentions of a skill in text (word boundary matching)"""
        # Use word boundaries to match complete words only
        pattern = r'\b' + re.escape(skill) + r'\b'
        matches = re.findall(pattern, text, re.IGNORECASE)
        return len(matches)
    
    def _fuzzy_match_skills(self, text: str) -> Dict[str, Dict]:
        """Find skills using fuzzy string matching with improved matching"""
        matched_skills = {}
        
        # Extract words from text (single and multi-word)
        single_words = re.findall(r'\b\w+\b', text.lower())
        multi_words = re.findall(r'\b\w+(?:\s+\w+){1,2}\b', text.lower())
        all_words = list(set(single_words + multi_words))
        
        for word in all_words:
            for skill in self.MASTER_SKILLS:
                # Calculate similarity score with lower threshold for better matching
                similarity = fuzz.token_set_ratio(word.lower(), skill.lower())
                
                # Lower threshold from 75 to 70 for better skill detection
                if similarity >= 70 and skill not in matched_skills:
                    mentions = self._find_skill_mentions(skill, text)
                    if mentions > 0:  # Only add if actually found in text
                        matched_skills[skill] = {
                            'score': similarity,
                            'occurrences': mentions
                        }
        
        return matched_skills
    
    def _semantic_match_skills(self, text: str) -> List[str]:
        """Find related skills based on semantic context"""
        semantic_groups = {
            'frontend': ['html', 'css', 'javascript', 'react', 'vue', 'angular'],
            'backend': ['python', 'java', 'node.js', 'django', 'spring'],
            'database': ['sql', 'mysql', 'mongodb', 'postgresql'],
            'devops': ['docker', 'kubernetes', 'jenkins', 'terraform'],
            'data': ['machine learning', 'data science', 'tensorflow', 'python'],
        }
        
        matched = []
        for group, skills in semantic_groups.items():
            if any(skill in text for skill in skills):
                matched.extend(skills)
        
        return list(set(matched))
    
    def get_top_skills(self, n: int = 10) -> List[Dict]:
        """Get top N extracted skills by confidence"""
        return self.extracted_skills[:n]
    
    def get_skill_confidence(self, skill: str) -> float:
        """Get confidence score for a specific skill"""
        for item in self.extracted_skills:
            if item['skill'].lower() == skill.lower():
                return item['confidence']
        return 0.0


# Module-level function for backward compatibility
def extract_skills(text: str) -> List[Dict]:
    """Extract skills from text"""
    extractor = SkillExtractor()
    return extractor.extract_skills(text)
