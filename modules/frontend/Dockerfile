FROM node:14.8.0-alpine3.12

WORKDIR .

COPY package.json ./
COPY package-lock.json ./

RUN npm install
RUN npm install react-scripts@3.4.3 -g

CMD ["pwd"]
COPY . ./
RUN chmod +x generate_env_script.sh
RUN chmod +x start.sh

EXPOSE 3000

CMD ["./start.sh"]

