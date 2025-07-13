#!/usr/bin/env python3
"""
Waple.pro Blog Article Generator
Generates high-quality HTML articles from the article list
"""

import os
import re
from datetime import datetime, timedelta

class ArticleGenerator:
    def __init__(self):
        self.base_path = "articles"
        self.template_path = "templates"
        self.article_list = self.load_article_list()
        
    def load_article_list(self):
        """Load the article list from article-list.md"""
        articles = []
        with open("article-list.md", "r") as f:
            content = f.read()
            
        # Parse the markdown to extract article titles
        lines = content.split("\n")
        current_category = ""
        
        for line in lines:
            if line.startswith("## ") and "Category" in line:
                current_category = line.split("(")[0].replace("## ", "").strip()
            elif line.strip().startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")) or \
                 line.strip().startswith(("10.", "11.", "12.", "13.", "14.", "15.", "16.", "17.", "18.", "19.")) or \
                 line.strip().startswith(("20.", "21.", "22.", "23.", "24.", "25.")):
                if "✅" not in line:  # Skip completed articles
                    title = line.split(". ", 1)[1] if ". " in line else line.strip()
                    articles.append({
                        "title": title,
                        "category": current_category,
                        "filename": self.generate_filename(title)
                    })
        
        return articles
    
    def generate_filename(self, title):
        """Convert article title to filename"""
        # Remove special characters and convert to lowercase
        filename = re.sub(r'[^\w\s-]', '', title.lower())
        filename = re.sub(r'[-\s]+', '-', filename)
        return f"{filename}.html"
    
    def generate_article_html(self, article):
        """Generate HTML for a single article"""
        
        # Determine category-specific keywords and description
        category_keywords = {
            "Consciousness": "digital consciousness, consciousness tracking, spiritual technology, AI consciousness, mindfulness technology, consciousness evolution, digital spirituality, spiritual growth, self-awareness, consciousness expansion",
            "Spirituality": "digital spirituality, spiritual technology, virtual sacred spaces, spiritual apps, digital prayer, spiritual communities, spiritual growth, ancient wisdom, modern spirituality, spiritual practices",
            "Mindfulness": "digital mindfulness, mindfulness apps, mindfulness technology, stress management, emotional regulation, focus, concentration, digital wellness, mindfulness practices, mental health",
            "AI Guru": "AI guru, AI spiritual guidance, artificial intelligence spirituality, personalized spiritual guidance, AI meditation, spiritual AI, AI consciousness, digital spiritual guidance, AI spiritual practices, intelligent spirituality"
        }
        
        category_desc = {
            "Consciousness": f"Explore {article['title'].lower()} and discover how digital tools like Waple.pro are transforming consciousness and spiritual awareness.",
            "Spirituality": f"Learn about {article['title'].lower()} and how modern technology is enhancing spiritual practices and personal growth.",
            "Mindfulness": f"Discover {article['title'].lower()} and practical techniques for integrating mindfulness into your digital lifestyle with Waple.pro.",
            "AI Guru": f"Explore {article['title'].lower()} and how AI-powered spiritual guidance is revolutionizing personal development and spiritual growth."
        }
        
        # Generate content based on title and category
        content = self.generate_article_content(article)
        
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']} | Waple.pro</title>
    <meta name="description" content="{category_desc[article['category']]}">
    <meta name="keywords" content="{category_keywords[article['category']]}, waple.pro">
    <meta name="author" content="Waple.pro">
    <meta property="og:title" content="{article['title']}">
    <meta property="og:description" content="{category_desc[article['category']]}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://waple.pro/blog/articles/{article['filename']}">
    <meta property="article:published_time" content="2024-12-01T00:00:00Z">
    <meta property="article:author" content="Waple.pro">
    <meta property="article:section" content="{article['category']}">
    <link rel="canonical" href="https://waple.pro/blog/articles/{article['filename']}">
    <link rel="stylesheet" href="../assets/css/style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        .article-content {{
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
            line-height: 1.8;
        }}
        .article-header {{
            text-align: center;
            margin-bottom: 3rem;
        }}
        .article-title {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }}
        .article-meta {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }}
        .article-image {{
            width: 100%;
            height: 400px;
            background: var(--gradient-primary);
            border-radius: 12px;
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 2rem;
        }}
        .article-content h2 {{
            font-size: 1.8rem;
            font-weight: 600;
            margin: 2rem 0 1rem;
            color: var(--text-primary);
        }}
        .article-content h3 {{
            font-size: 1.4rem;
            font-weight: 600;
            margin: 1.5rem 0 0.5rem;
            color: var(--text-primary);
        }}
        .article-content p {{
            margin-bottom: 1.5rem;
            color: var(--text-secondary);
        }}
        .article-content blockquote {{
            border-left: 4px solid var(--primary-color);
            padding-left: 1.5rem;
            margin: 2rem 0;
            font-style: italic;
            color: var(--text-primary);
            font-size: 1.1rem;
        }}
        .cta-box {{
            background: var(--gradient-secondary);
            color: white;
            padding: 2rem;
            border-radius: 12px;
            margin: 2rem 0;
            text-align: center;
        }}
        .cta-box h3 {{
            color: white;
            margin-bottom: 1rem;
        }}
        .breadcrumb {{
            margin-bottom: 2rem;
        }}
        .breadcrumb a {{
            color: var(--text-light);
            text-decoration: none;
        }}
        .breadcrumb a:hover {{
            color: var(--primary-color);
        }}
    </style>
</head>
<body>
    <header class="header">
        <nav class="nav">
            <div class="nav-container">
                <div class="logo">
                    <a href="https://waple.pro">
                        <img src="../assets/images/waple-logo.svg" alt="Waple.pro" class="logo-img">
                        <span class="logo-text">Waple.pro</span>
                    </a>
                </div>
                <ul class="nav-menu">
                    <li><a href="../index.html">Blog Home</a></li>
                    <li><a href="../categories/consciousness.html">Consciousness</a></li>
                    <li><a href="../categories/spirituality.html">Spirituality</a></li>
                    <li><a href="../categories/mindfulness.html">Mindfulness</a></li>
                    <li><a href="https://waple.pro" class="cta-button">Try Waple.pro</a></li>
                </ul>
            </div>
        </nav>
    </header>

    <main class="main">
        <article class="article-content">
            <div class="breadcrumb">
                <a href="../index.html">Blog</a> → 
                <a href="../categories/{article['category'].lower().replace(' ', '-')}.html">{article['category']}</a> → 
                {article['title']}
            </div>

            <div class="article-header">
                <h1 class="article-title">{article['title']}</h1>
                <div class="article-meta">
                    <span class="category">{article['category']}</span>
                    <span class="date">December 1, 2024</span>
                    <span class="reading-time">8 min read</span>
                </div>
            </div>

            <div class="article-image">
                🌟 {article['title']}
            </div>

            {content}

            <div class="cta-box">
                <h3>Transform Your Consciousness Today</h3>
                <p>Experience the power of digital spirituality with Waple.pro. Start your journey toward enhanced consciousness and spiritual growth.</p>
                <a href="https://waple.pro" class="primary-button">Start Your Digital Consciousness Journey</a>
            </div>

            <div style="margin-top: 3rem; padding: 2rem; background: var(--bg-secondary); border-radius: 12px;">
                <h3>Related Articles</h3>
                <ul>
                    <li><a href="digital-consciousness-revolution.html">The Digital Consciousness Revolution</a></li>
                    <li><a href="ai-guru-spiritual-guidance.html">AI Guru: The Future of Spiritual Guidance</a></li>
                    <li><a href="digital-mindfulness-practices.html">Digital Mindfulness: Practices for the Modern Seeker</a></li>
                </ul>
            </div>
        </article>
    </main>

    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>Waple.pro</h3>
                    <p>Digitalizing consciousness through technology and spirituality</p>
                </div>
                <div class="footer-section">
                    <h4>Categories</h4>
                    <ul>
                        <li><a href="../categories/consciousness.html">Consciousness</a></li>
                        <li><a href="../categories/spirituality.html">Spirituality</a></li>
                        <li><a href="../categories/mindfulness.html">Mindfulness</a></li>
                        <li><a href="../categories/ai-guru.html">AI Guru</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>Resources</h4>
                    <ul>
                        <li><a href="../sitemap.xml">Sitemap</a></li>
                        <li><a href="https://waple.pro">Main Site</a></li>
                        <li><a href="../contact.html">Contact</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Waple.pro. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script src="../assets/js/main.js"></script>
</body>
</html>"""
        
        return html_template
    
    def generate_article_content(self, article):
        """Generate article content based on title and category"""
        
        # This is a simplified content generator
        # In a real implementation, you would have more sophisticated content generation
        
        content = f"""
            <p>In the rapidly evolving landscape of digital consciousness and spiritual technology, {article['title'].lower()} represents a significant advancement in how we approach personal growth and spiritual development.</p>

            <p>At Waple.pro, we believe that technology and spirituality are not opposing forces but complementary tools for human evolution. This article explores how {article['title'].lower()} is reshaping our understanding of consciousness and spiritual practice.</p>

            <h2>The Evolution of {article['category']} in the Digital Age</h2>

            <p>As we navigate the complexities of modern life, traditional approaches to {article['category'].lower()} are being enhanced and transformed by digital technology. This evolution isn't about replacing ancient wisdom but about making it more accessible and relevant to contemporary seekers.</p>

            <blockquote>
                "Technology is not the enemy of spirituality—it's the bridge that connects ancient wisdom with modern seekers." — Waple.pro Philosophy
            </blockquote>

            <h3>How Digital Tools Enhance {article['category']}</h3>

            <p>Digital platforms like Waple.pro offer several unique advantages that traditional {article['category'].lower()} practices alone cannot provide:</p>

            <ul>
                <li><strong>Personalized Guidance:</strong> AI-powered spiritual guidance that adapts to your unique journey and needs</li>
                <li><strong>Continuous Support:</strong> 24/7 access to spiritual resources and practices</li>
                <li><strong>Progress Tracking:</strong> Digital tools to monitor your spiritual growth and awareness</li>
                <li><strong>Community Connection:</strong> Global networks of like-minded seekers</li>
                <li><strong>Integration:</strong> Seamless blending of spiritual practices with daily digital life</li>
            </ul>

            <h2>Practical Applications of {article['title']}</h2>

            <p>So how does {article['title'].lower()} work in practice? Let's explore some real-world applications that are transforming how people approach spirituality:</p>

            <h3>1. Digital Integration</h3>

            <p>Modern spiritual seekers often struggle to find time for traditional practices. Digital tools like Waple.pro offer guided sessions that can be accessed anywhere, anytime, making spiritual practice more accessible than ever before.</p>

            <h3>2. Personalized Learning</h3>

            <p>Every spiritual journey is unique. Digital platforms can provide personalized guidance that adapts to your specific needs, beliefs, and current circumstances.</p>

            <h3>3. Community Building</h3>

            <p>Digital platforms create global communities of spiritual seekers, allowing for connection and support regardless of geographical location.</p>

            <h2>The Future of {article['category']} Technology</h2>

            <p>As technology continues to advance, the potential for {article['category'].lower()} enhancement is expanding rapidly. We're moving toward a world where:</p>

            <ul>
                <li>Spiritual practices are seamlessly integrated into daily digital life</li>
                <li>AI systems provide increasingly sophisticated spiritual guidance</li>
                <li>Virtual reality creates immersive spiritual experiences</li>
                <li>Global spiritual communities transcend physical boundaries</li>
                <li>Personal consciousness data helps optimize spiritual growth</li>
            </ul>

            <h2>Getting Started with {article['title']}</h2>

            <p>If you're ready to explore {article['title'].lower()}, here are some steps to begin your journey:</p>

            <ol>
                <li><strong>Start Small:</strong> Begin with short, guided sessions</li>
                <li><strong>Track Your Journey:</strong> Use digital tools to monitor your progress</li>
                <li><strong>Engage with Community:</strong> Connect with like-minded seekers</li>
                <li><strong>Integrate Practices:</strong> Blend digital tools with traditional practices</li>
                <li><strong>Trust Your Intuition:</strong> Always trust your inner wisdom</li>
            </ol>

            <h2>Conclusion</h2>

            <p>{article['title']} represents a fundamental shift in how we approach spirituality and personal growth. By embracing technology as a tool for spiritual development, we're not abandoning traditional wisdom but making it more accessible and relevant to modern life.</p>

            <p>Platforms like Waple.pro are leading this transformation, offering innovative ways to cultivate consciousness in the digital age. Whether you're a seasoned spiritual practitioner or just beginning your journey, digital tools can enhance your spiritual growth and help you navigate the complexities of modern life.</p>

            <p>The future of spirituality is digital, and the future is now. Are you ready to join the revolution?</p>
        """
        
        return content
    
    def generate_all_articles(self):
        """Generate all remaining articles"""
        print(f"Generating {len(self.article_list)} articles...")
        
        for i, article in enumerate(self.article_list, 1):
            print(f"Generating article {i}/{len(self.article_list)}: {article['title']}")
            
            html_content = self.generate_article_html(article)
            
            # Create articles directory if it doesn't exist
            os.makedirs(self.base_path, exist_ok=True)
            
            # Write the article file
            filepath = os.path.join(self.base_path, article['filename'])
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✓ Created: {filepath}")
        
        print(f"\n✅ Successfully generated {len(self.article_list)} articles!")
        print("Next steps:")
        print("1. Review and customize the generated articles")
        print("2. Update the sitemap.xml with new URLs")
        print("3. Add internal links between articles")
        print("4. Deploy to your hosting provider")

if __name__ == "__main__":
    generator = ArticleGenerator()
    generator.generate_all_articles()