FROM arm64v8/debian:12

# 避免交互
ENV DEBIAN_FRONTEND=noninteractive

# 安装系统依赖
RUN apt update && apt install -y \
    curl \
    wget \
    build-essential \
    file \
    libssl-dev \
    libgtk-3-dev \
    libayatana-appindicator3-dev \
    librsvg2-dev \
    libwebkit2gtk-4.1-dev \
    git \
    ca-certificates \
    xz-utils \
    && rm -rf /var/lib/apt/lists/*

# 安装 Node（用官方二进制，避免 nvm）
RUN curl -fsSL https://nodejs.org/dist/v20.11.1/node-v20.11.1-linux-arm64.tar.xz | tar -xJ -C /usr/local --strip-components=1

# 安装 yarn
RUN npm install -g yarn

# 安装 Rust
RUN curl https://sh.rustup.rs -sSf | sh -y
ENV PATH="/root/.cargo/bin:${PATH}"

# 设置工作目录
WORKDIR /app

# 拷贝项目
COPY . .

# 安装前端依赖
RUN yarn install

# 构建前端（可选优化）
RUN yarn build

# 默认执行打包
CMD ["yarn", "build:exe"]