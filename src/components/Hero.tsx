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
          <h1 className="text-6xl md:text-7xl font-bold mb-6 leading-tight">
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
            whileTap={{ scale: 0.95 }}
            onClick={onStartChat}
            className="group shimmer-button shimmer-button-dark bg-gray-900 text-white px-4 py-2 rounded-lg font-medium text-sm flex items-center space-x-1 transition-all duration-300 shadow-lg"
          >
            <span>Start Conversation</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </motion.button>
          
          <motion.button
            whileTap={{ scale: 0.95 }}
            className="shimmer-button bg-white border border-gray-200 text-gray-900 px-4 py-2 rounded-lg font-medium text-sm transition-all duration-300 shadow-md"
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
            { icon: Brain, title: "Advanced Reasoning", desc: "Multi-step problem solving with Claude Sonnet 4" },
            { icon: Zap, title: "Real-time Execution", desc: "Live code execution and web interaction" },
            { icon: Sparkles, title: "Multi-modal", desc: "Text, images, audio, and video processing" }
          ].map((feature, index) => (
            <motion.div
              key={index}
              whileHover={{ y: -5, scale: 1.02 }}
              whileHover={{ y: -5 }}
              className="bg-white rounded-2xl p-8 group transition-all duration-300 shadow-lg border border-gray-200"
            >
              <div className="flex items-center justify-center mb-6">
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