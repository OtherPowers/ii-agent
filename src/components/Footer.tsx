import React from 'react'
import { motion } from 'framer-motion'
import { Github, Twitter, Globe, Heart } from 'lucide-react'

const Footer = () => {
  return (
    <footer className="py-16 px-6 border-t border-white/10">
      <div className="container mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12"
        >
          <div className="md:col-span-2">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-400 to-purple-600 rounded-xl flex items-center justify-center">
                <span className="text-white font-bold text-lg">II</span>
              </div>
              <div>
                <h3 className="text-xl font-bold text-white">II-Agent</h3>
                <p className="text-white/60 text-sm">Intelligent Assistant Platform</p>
              </div>
            </div>
            <p className="text-white/70 leading-relaxed max-w-md">
              Open-source intelligent assistant designed to streamline and enhance workflows 
              across multiple domains with advanced AI capabilities.
            </p>
          </div>
          
          <div>
            <h4 className="text-white font-semibold mb-4">Resources</h4>
            <ul className="space-y-2">
              {['Documentation', 'API Reference', 'Examples', 'Community'].map((item) => (
                <li key={item}>
                  <motion.a
                    whileHover={{ x: 5 }}
                    href="#"
                    className="text-white/60 hover:text-white transition-colors"
                  >
                    {item}
                  </motion.a>
                </li>
              ))}
            </ul>
          </div>
          
          <div>
            <h4 className="text-white font-semibold mb-4">Connect</h4>
            <div className="flex space-x-4">
              {[
                { icon: Github, href: 'https://github.com/Intelligent-Internet/ii-agent' },
                { icon: Twitter, href: '#' },
                { icon: Globe, href: 'https://ii.inc' }
              ].map((social, index) => (
                <motion.a
                  key={index}
                  whileHover={{ scale: 1.1, y: -2 }}
                  whileTap={{ scale: 0.95 }}
                  href={social.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="p-3 glass-effect rounded-xl text-white/80 hover:text-white transition-colors"
                >
                  <social.icon className="w-5 h-5" />
                </motion.a>
              ))}
            </div>
          </div>
        </motion.div>
        
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="pt-8 border-t border-white/10 flex flex-col md:flex-row items-center justify-between"
        >
          <p className="text-white/60 text-sm mb-4 md:mb-0">
            © 2025 Intelligent Internet. All rights reserved.
          </p>
          
          <div className="flex items-center space-x-2 text-white/60 text-sm">
            <span>Made with</span>
            <Heart className="w-4 h-4 text-red-400" />
            <span>by the II team</span>
          </div>
        </motion.div>
      </div>
    </footer>
  )
}

export default Footer