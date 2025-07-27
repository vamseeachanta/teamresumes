# Content Generation Agent Prompt Templates

> Specialized prompts for LinkedIn posts, professional bios, and social media content generation
> Version: 1.0.0
> Created: 2025-07-27

## LinkedIn Post Generation

### Achievement Spotlight Prompt

```
Generate a LinkedIn post highlighting a specific achievement from the resume `{file_path}`:

**Requirements:**
- Focus on quantified achievements with metrics
- Include the challenge, approach, and result
- Add relevant hashtags (5-8 maximum)
- Keep under 3000 characters
- Use professional but engaging tone
- End with a question to encourage engagement

**Template Structure:**
1. Opening hook with emoji
2. Achievement details with context
3. Key lessons learned or insights
4. Call-to-action question
5. Relevant hashtags

**Tone:** Professional, confident, humble
**Style:** Storytelling with data-driven impact
```

### Skills Showcase Prompt

```
Create a LinkedIn post showcasing technical skills from `{file_path}`:

**Focus Areas:**
- Highlight 3-5 core technical skills
- Connect skills to real-world impact
- Mention years of experience or expertise level
- Include technology evolution perspective
- Add industry-relevant hashtags

**Content Framework:**
- Tech stack spotlight introduction
- Brief context of how skills are applied
- Impact or results achieved using these skills
- Future learning interests or curiosity
- Engagement question about others' tech stacks

**Character limit:** 3000
**Hashtags:** Include both technology-specific and role-based tags
```

### Career Update Prompt

```
Generate a professional career update post from `{file_path}`:

**Content Elements:**
- Current role and company (if appropriate to share)
- Recent key accomplishments or milestones
- Professional growth highlights
- Gratitude and forward-looking statement
- Networking call-to-action

**Style Guidelines:**
- Authentic and personal while maintaining professionalism
- Focus on value delivered rather than just responsibilities
- Include 2-3 specific achievements with impact
- Express enthusiasm for future opportunities
- Invite professional connections and conversations

**Length:** 300-500 words ideal for LinkedIn engagement
```

## Professional Bio Generation

### Executive Bio Prompt

```
Create a comprehensive executive biography from `{file_path}`:

**Structure Requirements:**
- Opening statement with current role and value proposition
- Career progression and key leadership roles
- Quantified achievements and business impact
- Education and relevant credentials
- Industry expertise and thought leadership
- Personal mission or philosophy
- Current focus areas and future vision

**Length Options:**
- Short (100-150 words): For speaker bios, team pages
- Medium (200-300 words): For conference profiles, board positions
- Long (400-500 words): For detailed leadership profiles

**Tone:** Authoritative, accomplished, forward-thinking
```

### Team Member Bio Prompt

```
Generate a team member biography from `{file_path}`:

**Key Components:**
- Name and current role
- Educational background
- Core expertise and specializations
- Notable projects or achievements
- Years of experience in relevant areas
- Personal interests or values (if appropriate)

**Use Cases:**
- Company website team pages
- Project introductions
- Client presentations
- Conference speaker profiles

**Length:** 75-200 words
**Style:** Professional but approachable, third-person
```

### Social Media Bio Prompt

```
Create optimized social media bio variations from `{file_path}`:

**Platform-Specific Formats:**

**LinkedIn Headline (220 characters):**
- Current role + key value proposition
- Include relevant keywords for discovery
- Professional but personality-driven

**LinkedIn Summary (2600 characters):**
- Expanded professional story
- Career journey and achievements
- Skills and expertise
- Personal mission and values
- Call-to-action for connections

**Twitter/X Bio (160 characters):**
- Concise role + personality
- Key expertise areas
- Optional personal touch

Generate 3 variations for each platform.
```

## Social Media Content

### Twitter Thread Prompt

```
Create a Twitter/X thread from achievements in `{file_path}`:

**Thread Structure:**
1. Hook tweet introducing the topic (with thread indicator 🧵)
2. 3-5 detail tweets expanding on key achievements
3. Insight or lesson learned tweet
4. Closing tweet with engagement question

**Tweet Requirements:**
- Each tweet under 280 characters
- Progressive narrative flow
- Include relevant emojis for visual appeal
- End thread with question to encourage replies
- Use hashtags sparingly (1-2 per tweet max)

**Topics to Cover:**
- Professional wins with metrics
- Lessons learned from challenges
- Industry insights or trends
- Career development journey
```

### Content Calendar Prompt

```
Generate a month-long content calendar using data from `{file_path}`:

**Weekly Themes:**
- Week 1: Achievement spotlight and professional wins
- Week 2: Skills and expertise showcase
- Week 3: Industry insights and thought leadership
- Week 4: Career journey and lessons learned

**Content Types to Include:**
- LinkedIn posts (2-3 per week)
- Twitter threads (1 per week)
- Professional updates
- Engagement-driven posts
- Value-sharing content

**Specify for Each Post:**
- Optimal posting day/time
- Content type and format
- Key message or theme
- Relevant hashtags
- Expected engagement style

**Output Format:** Calendar table with dates, post types, topics, and hashtags
```

## Industry-Specific Content

### Tech Industry Content

```
Generate technology-focused content from `{file_path}`:

**Content Areas:**
- Technical achievements and innovations
- Open source contributions or projects
- Technology trends and insights
- Development best practices
- Team leadership in tech environments
- Continuous learning and skill development

**Platform Adaptations:**
- LinkedIn: Professional achievements with technical depth
- Twitter: Quick insights and tech opinions
- GitHub: Project showcases and contributions
- Dev.to: Technical tutorials and experiences

**Hashtag Strategy:**
- Technology-specific: #Python, #React, #AWS, #DevOps
- Role-based: #SoftwareEngineering, #TechLead, #FullStack
- Industry: #TechCommunity, #Innovation, #OpenSource
```

### Leadership Content

```
Create leadership-focused content from `{file_path}`:

**Leadership Themes:**
- Team building and people management
- Strategic decision making
- Change management and transformation
- Mentoring and development
- Cross-functional collaboration
- Results-driven leadership

**Content Formats:**
- Leadership lessons learned
- Team success stories
- Management philosophy posts
- Industry leadership insights
- Mentorship experiences
- Organizational impact stories

**Audience Considerations:**
- Other leaders and managers
- Team members and direct reports
- Industry peers and network
- Potential recruits and talent
```

## Content Enhancement

### Engagement Optimization

```
Enhance content for maximum LinkedIn engagement using `{file_path}`:

**Engagement Tactics:**
- Start with attention-grabbing first line
- Use storytelling structure (challenge → solution → result)
- Include specific metrics and quantifiable outcomes
- Add personal insights or lessons learned
- End with thought-provoking question
- Use line breaks for readability
- Include relevant emojis strategically

**Content Psychology:**
- Appeal to professional aspirations
- Share relatable challenges and solutions
- Provide actionable insights or tips
- Create curiosity and discussion
- Establish thought leadership credibility

**Call-to-Action Examples:**
- "What's been your biggest professional breakthrough this year?"
- "How do you approach [relevant challenge] in your organization?"
- "What would you add to this list?"
```

### Brand Voice Development

```
Develop consistent brand voice for content from `{file_path}`:

**Voice Characteristics:**
- Professional but approachable
- Confident without being arrogant
- Knowledgeable and helpful
- Authentic and relatable
- Forward-thinking and innovative

**Tone Variations:**
- Achievement posts: Proud but humble
- Insight sharing: Thoughtful and analytical
- Team posts: Collaborative and appreciative
- Industry commentary: Informed and balanced

**Language Guidelines:**
- Use active voice and strong action verbs
- Avoid jargon unless explaining it
- Include personal pronouns appropriately
- Balance confidence with humility
- Maintain consistency across all content
```

## Variables for Dynamic Prompts

```yaml
# Available variables for prompt customization
variables:
  file_path: "Path to the resume file being processed"
  content_type: "linkedin_post | bio | twitter_thread | calendar"
  post_theme: "achievement | skills | career_update | thought_leadership"
  length_target: "short | medium | long | character_limit"
  audience: "professional | technical | leadership | general"
  industry: "technology | finance | healthcare | consulting"
  
# Usage examples:
# {file_path} -> "cv/john_smith_resume.md"
# {content_type} -> "linkedin_post"
# {post_theme} -> "achievement"
```

## Integration Prompts

### With Resume Processing Agent
```
Coordinate with resume processing agent to generate content from validated resume data in `{file_path}`:

**Process:**
1. Verify resume has been validated and is of good quality
2. Extract only quantified achievements and verified skills
3. Use professional language assessment results
4. Generate content that addresses any professional tone issues found
5. Ensure all generated content maintains high professional standards
```

### With Documentation Agent
```
Work with documentation agent to update project documentation with generated content:

**Tasks:**
- Update team member profiles with new bios
- Add content samples to documentation
- Create content generation guidelines
- Maintain cross-references to generated content files
- Ensure all links and references are functional
```

## Quality Assurance Prompts

### Content Review Checklist

```
Review generated content for quality and effectiveness:

**Professional Standards:**
- Appropriate tone for target platform
- Grammatically correct and well-written
- Free of typos and formatting errors
- Consistent with professional brand
- Adheres to platform character limits

**Engagement Potential:**
- Compelling opening that grabs attention
- Clear value proposition or insight
- Relevant and targeted hashtags
- Appropriate call-to-action
- Likely to generate meaningful engagement

**Content Authenticity:**
- Based on actual resume achievements
- Reflects genuine professional experience
- Maintains honest and humble tone
- Avoids exaggeration or false claims
- Aligns with overall professional narrative
```

### A/B Testing Framework

```
Create content variations for testing effectiveness:

**Variation Types:**
- Different opening hooks
- Alternative storytelling approaches
- Varying hashtag strategies
- Different call-to-action styles
- Various content lengths

**Testing Metrics:**
- Engagement rate (likes, comments, shares)
- Reach and impressions
- Click-through rates (if applicable)
- Quality of comments and discussions
- New connections or followers gained

**Generate 2-3 variations for each major content piece to enable testing and optimization.**
```