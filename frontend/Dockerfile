# Dockerfile for Angular Frontend

# Sử dụng Node.js 18
FROM node:18 AS build

# Đặt thư mục làm việc
WORKDIR /app

# Sao chép package.json và cài đặt các phụ thuộc
COPY package*.json ./

RUN npm install

# Sao chép mã nguồn của bạn vào container
COPY . .

# Build ứng dụng Angular
RUN npm run build --prod --output-hashing=all

# Tạo một image mới với Nginx để phục vụ ứng dụng
FROM nginx:alpine

# Sao chép build từ bước trước vào thư mục Nginx
COPY --from=build /app/dist/* /usr/share/nginx/html

COPY ./nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80
