# Mini Project: Weather report web application
This is a cloud computing coursework.

The project provides python flask RESTful API for detailed whether forcast information. It uses external RESTful service (see below) to get data.

The external API is from [QWeather](https://dev.qweather.com/en/). 




## 1. Basic Tasks

### 1.1 External API

```
url_api_weather = 'https://devapi.qweather.com/v7/weather/'
url_api_geo = 'https://geoapi.qweather.com/v2/city/'
```
This api interacts with external [QWeather](https://dev.qweather.com/en/) api. It provides whether information, including ***location, weather temperature, feels like temperature***, which will be interpreted later in the app when being requested.

### 1.2 External Cloud Database

In this project, we choose MySQL for holding persisting user information, including ***Table user and blacklist***. This database is deployed on cloud via Google Cloud Platform.

#### 1.2.1 Google Cloud Platform MySQL instance Set Up

Create SQL instance through GCP and get the ip address of  the SQL server. and then add the instance ip to connect to SQL server.



#### 1.2.2 Implement Interface In Python

Four different kinds of HTTP request corresponding to four operations on database. Interface including ```read```, ```write```, ```update```, ```delete``` methods.

```
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@34.88.54.129:3306/db"
```



### 1.3 CURD Operations

Test for REST api will be carried out using postman. In each section, the body of the request will be shown. In this section, we use postman to show how to do GET, POST, PUT and DELETE.

#### 1.3.1 POST
Request Body:
```
{
    "name": "nameabc",
    "username": "userabc",
    "password": "passowrdabc",
    "email": "userabc@example.com",
    "pincode": "000000",
    "phoneNumber": "8888888888",
    "address": "London"
}
```
Response Body:
```
{
	"message":"Registration Successful"
}
```

It returns .
#### 1.3.2 GET

```
 https://34.136.206.122:5000/
```

Response Body:
```
"This is a project of Group 28"
```
#### 1.3.3 PUT
Request Body:
```
{
    "userIdentity": "userabcdefg@example.com",
    "existedPassword": "passowrdabcdefg",
    "newPassword": "11111111111"
}
```


Response Body:
```
{
    "message": "Change Successful"
}
```

To proof that PUT request does work, use GET request again to verify.

#### 1.3.4 DELETE
```
def delete():
    black = Blacklist.query.first()
    db.session.delete(black)
    db.session.commit()
```



## 2. Implementing additional features
### 2.1 HTTPS Implementation

To set up HTTPS service, run the following command to generate self-signed SSL certificate.

```
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

Modify app.py as below to make https available.

```
if __name__ == '__main__':
    # Create app.
    app = create_app()
    context = ("cert.pem", "key.pem")

    # Run app. For production use another web server.
    # Set debug and use_reloader parameters as False.
    app.run(port=5000, debug=True, host='0.0.0.0', use_reloader=True,ssl_context=context)
```

Now the service can be accessed through HTTPS.

### 2.2 Hash-Based Authentication

A complete hash-based authentication includes two stage.

#### 2.2.1 Apply for an unique token

```
    def generate_auth_token(self):
        return jwt.dumps({"email": self.email})

    @staticmethod
    @auth.verify_token
    def verify_auth_token(token):
        try:
            data = jwt.loads(token)
        except:
            return False

        if (Blacklist.check_blacklist(token)):
            return False

        if "email" in data:
            return True
        return False
```

After requeset is sent, flask would return an unique token. Authentication use Basic Auth.



#### 2.2.2 Logout through token

```
class Logout(Resource):
    @staticmethod
    @auth.login_required
    def post():
        # get auth token
        auth_token = request.json.get("token")
        blacklist_token = Blacklist(token=auth_token, blackisted_on=datetime.utcnow())
        try:
            # insert the token
            db.session.add(blacklist_token)
            db.session.commit()
            return make_response(LOGOUT_SUCCESSFUL)
        except Exception as e:
            return make_response(ERROR_ON_HANDLING)
```

### 2.3 User Accounts And Access Management

In most situations, every user should register and then has the authority to login and log out. When the user want to edit password, he should input old password and new password to check.

