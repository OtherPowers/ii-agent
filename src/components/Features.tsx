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
      color: "bg-blue-100"
    },
    {
      icon: Code,
      title: "Software Development",
      description: "Full-stack development, code generation, debugging, and automated testing across multiple languages.",
      color: "bg-green-100"
    },
    {
      icon: Globe,
      title: "Web Automation",
      description: "Browser automation, web scraping, and dynamic website creation with live deployment.",
      color: "bg-purple-100"
    },
    {
      icon: FileText,
      title: "Content Creation",
      description: "Technical documentation, articles, presentations, and multimedia content generation.",
      color: "bg-orange-100"
    },
    {
      icon: Database,
      title: "Data Processing",
      description: "Advanced data manipulation, visualization, and automated report generation.",
      color: "bg-teal-100"
    },
    {
      icon: Terminal,
      title: "System Operations",
      description: "Command-line automation, file management, and workflow optimization.",
      color: "bg-gray-100"
    },
    {
      icon: Palette,
      title: "Media Generation",
      description: "AI-powered image, video, and audio generation with professional quality output.",
      color: "bg-pink-100"
    },
    {
      icon: Layers,
      title: "Multi-modal AI",
      description: "Process and understand text, images, audio, video, and documents seamlessly.",
      color: "bg-indigo-100"
    },
    {
      icon: Workflow,
      title: "Task Automation",
      description: "Complex workflow automation with intelligent decision-making and error handling.",
      color: "bg-yellow-100"
    }
  ]

  return (
    <section id="features" className="py-20 px-6">
      <div className="container-custom">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Comprehensive <span className="gradient-text">Capabilities</span>
          </h2>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto text-balance">
            II-Agent excels across multiple domains, providing intelligent assistance 
            for complex tasks that require reasoning, creativity, and technical expertise.
          </p>
        </motion.div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            viewport={{ once: true }}
            className="text-center"
          >
            <h3 className="text-2xl font-bold text-gray-900 mb-4">Research & Analysis</h3>
            <p className="text-gray-600 leading-relaxed">
              Deep web research, fact-checking, and comprehensive data analysis with multi-source verification and structured reporting.
            </p>
          </motion.div>
          
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            viewport={{ once: true }}
            className="text-center"
          >
            <h3 className="text-2xl font-bold text-gray-900 mb-4">Development & Automation</h3>
            <p className="text-gray-600 leading-relaxed">
              Full-stack development, code generation, debugging, testing, and workflow automation across multiple programming languages.
            </p>
          </motion.div>
          
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            viewport={{ once: true }}
            className="text-center"
          >
            <h3 className="text-2xl font-bold text-gray-900 mb-4">Content & Media</h3>
            <p className="text-gray-600 leading-relaxed">
              Technical documentation, multimedia content creation, presentations, and AI-powered media generation with professional quality.
            </p>
          </motion.div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              whileHover={{ y: -8, scale: 1.02 }}
              className="bg-white rounded-2xl p-8 group transition-all duration-300 webflow-shadow-lg smooth-hover border border-gray-200"
            >
              <div className={`w-12 h-12 ${feature.color} rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-all duration-300`}>
                <feature.icon className="w-6 h-6 text-gray-700" />
              </div>
              
              <h3 className="text-xl font-semibold text-gray-900 mb-4 transition-all duration-300">
                {feature.title}
              </h3>
              
              <p className="text-gray-600 leading-relaxed">
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