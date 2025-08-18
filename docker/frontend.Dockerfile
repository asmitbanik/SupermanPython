FROM node:20-alpine AS build
WORKDIR /app
COPY frontend/ /app/
RUN npm install && npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=build /app ./
EXPOSE 3000
ENV NEXT_PUBLIC_BACKEND_URL=http://backend:5000
CMD ["npm","start"]
