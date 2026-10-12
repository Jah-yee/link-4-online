import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  build:{
    rolldownOptions:{
      output:{
        minify:{
          compress:{
            dropConsole:true
          }
        }
      }
    }
  },
  html: {
    cspNonce: "__NONCE__"
  },
  server:{
    port:5173,
    strictPort:true,
  }
});
