import { defineConfig } from 'vite'

export default defineConfig({
  root: 'src', // Говорим Vite, что всё лежит в src
  build: {
    outDir: '../dist', // Собирать проект в папку dist в корне
  }
})