FROM node:20-slim

WORKDIR /app

# Копируем и устанавливаем зависимости от root
COPY package*.json ./
RUN npm install

# Копируем остальные файлы
COPY . .

# Даем права на выполнение для бинарников в node_modules
RUN chmod +x node_modules/.bin/*

# Меняем владельца на существующего пользователя node
RUN chown -R node:node /app

USER node

EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]