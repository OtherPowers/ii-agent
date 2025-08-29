import React from 'react'
import { motion } from 'framer-motion'
import { ArrowRight, Sparkles, Zap, Brain } from 'lucide-react'

interface HeroProps {
  onStartChat: () => void
}

const Hero = ({ onStartChat }: HeroProps) => {
  return (
    <section className="pt-32 pb-20 px-6">
      <div className="container-custom text-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="mb-8"
        >
          <div className="inline-flex items-center space-x-2 bg-gray-100 rounded-full px-4 py-2 mb-6 webflow-shadow">
            <Sparkles className="w-4 h-4 text-gray-700" />
            <span className="text-gray-700 text-sm">Powered by Advanced AI and Humans who believe in less awful futures (together)</span>
          </div>
          
          <h1 className="text-6xl md:text-7xl font-bold mb-6 leading-tight">
            <span className="text-gray-900" style={{ fontSize: 'calc(1em - 4px)' }}>Intelligent Internet Platform</span>
          </h1>
          
          <p className="text-lg text-gray-600 max-w-3xl mx-auto mb-8 text-balance">
            Experience the future of AI assistance with II-Agent. From research and content creation 
            to software development and workflow automation—all powered by cutting-edge language models.
          </p>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-6 mb-16"
        >
          <motion.button
            whileHover={{ scale: 1.05, boxShadow: "0 20px 40px rgba(34, 34, 34, 0.15)" }}
            whileTap={{ scale: 0.95 }}
            onClick={onStartChat}
            className="group bg-gray-900 text-white px-8 py-4 rounded-2xl font-semibold text-lg flex items-center space-x-2 glow-effect transition-all duration-300 webflow-shadow-lg smooth-hover"
          >
            <span>Start Conversation</span>
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </motion.button>
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="bg-white border border-gray-200 text-gray-900 px-8 py-4 rounded-2xl font-semibold text-lg hover:bg-gray-50 transition-all duration-300 webflow-shadow smooth-hover"
          >
            View Documentation
          </motion.button>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto"
        >
          {[
            { icon: Brain, title: "Advanced Reasoning", desc: "Multi-step problem solving with Claude Sonnet 4", color: "bg-blue-100" },
            { icon: Zap, title: "Real-time Execution", desc: "Live code execution and web interaction", color: "bg-green-100" },
            { icon: Sparkles, title: "Multi-modal", desc: "Text, images, audio, and video processing", color: "bg-purple-100" }
          ].map((feature, index) => (
            <motion.div
              key={index}
              whileHover={{ y: -5, scale: 1.02 }}
              className="bg-white rounded-2xl p-8 group hover:glow-effect transition-all duration-300 webflow-shadow smooth-hover border border-gray-200"
              className="bg-white rounded-2xl p-8 group transition-all duration-300 webflow-shadow smooth-hover border border-gray-200"
            >
              <div className={`w-12 h-12 ${feature.color} rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-all duration-300`}>
                <feature.icon className="w-6 h-6 text-gray-700" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4 transition-all duration-300">{feature.title}</h3>
              <p className="text-gray-600 leading-relaxed">{feature.desc}</p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  )
}

export default Hero