import React from 'react'
import { motion } from 'framer-motion'
import { 
  Code, 
  Search, 
  FileText, 
  Globe, 
  Database, 
  Palette,
  Terminal,
  Layers,
  Workflow
} from 'lucide-react'

const Features = () => {
  const features = [
    {
      icon: Search,
      title: "Research & Analysis",
      description: "Deep web research, fact-checking, and comprehensive data analysis with source verification.",
      color: "from-blue-500 to-cyan-500"
    },
    {
      icon: Code,
      title: "Software Development",
      description: "Full-stack development, code generation, debugging, and automated testing across multiple languages.",
      color: "from-green-500 to-emerald-500"
    },
    {
      icon: Globe,
      title: "Web Automation",
      description: "Browser automation, web scraping, and dynamic website creation with live deployment.",
      color: "from-purple-500 to-violet-500"
    },
    {
      icon: FileText,
      title: "Content Creation",
      description: "Technical documentation, articles, presentations, and multimedia content generation.",
      color: "from-orange-500 to-red-500"
    },
    {
      icon: Database,
      title: "Data Processing",
      description: "Advanced data manipulation, visualization, and automated report generation.",
      color: "from-teal-500 to-blue-500"
    },
    {
      icon: Terminal,
      title: "System Operations",
      description: "Command-line automation, file management, and workflow optimization.",
      color: "from-gray-500 to-slate-500"
    },
    {
      icon: Palette,
      title: "Media Generation",
      description: "AI-powered image, video, and audio generation with professional quality output.",
      color: "from-pink-500 to-rose-500"
    },
    {
      icon: Layers,
      title: "Multi-modal AI",
      description: "Process and understand text, images, audio, video, and documents seamlessly.",
      color: "from-indigo-500 to-purple-500"
    },
    {
      icon: Workflow,
      title: "Task Automation",
      description: "Complex workflow automation with intelligent decision-making and error handling.",
      color: "from-yellow-500 to-orange-500"
    }
  ]

  return (
    <section id="features" className="py-20 px-6">
      <div className="container mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Comprehensive <span className="gradient-text">Capabilities</span>
          </h2>
          <p className="text-xl text-white/70 max-w-3xl mx-auto text-balance">
            II-Agent excels across multiple domains, providing intelligent assistance 
            for complex tasks that require reasoning, creativity, and technical expertise.
          </p>
        </motion.div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              whileHover={{ y: -8, scale: 1.02 }}
              className="glass-effect rounded-2xl p-8 group hover:glow-effect transition-all duration-300"
            >
              <div className={`w-12 h-12 bg-gradient-to-r ${feature.color} rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                <feature.icon className="w-6 h-6 text-white" />
              </div>
              
              <h3 className="text-xl font-semibold text-white mb-4 group-hover:gradient-text transition-all duration-300">
                {feature.title}
              </h3>
              
              <p className="text-white/70 leading-relaxed">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}

export default Features