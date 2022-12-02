# pull official base image
#FROM node:13.12.0-alpine
FROM node:16.17.1-alpine
ARG BACKEND
# set working directory
WORKDIR /app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm install --silent

RUN npm install --save bootstrap@5.2.2 js-cookie@3.0.1 react-paginate@8.1.3 --silent

# add app
COPY . ./

#RUN BACKEND=${BACKEND}

# start app
CMD ["npm", "start"]