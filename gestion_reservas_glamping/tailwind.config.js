

module.exports = {
  content: [
    './templates/**/*.html',  // Ruta a las plantillas de Django
  ],
  theme: {
    extend: {
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
      screens: {
        'custom': '1060px', // Ajusta a tu tamaño deseado
      },
    },
  },
  plugins: [
    require('daisyui'),
  ],
  daisyui: {
    themes: ["autumn"],
  },
}
