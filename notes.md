## Notes
Some useful things
Auth
* https://saasitive.com/tutorial/react-token-based-authentication-django/
* https://inmagik.com/it/blog/django-rest-and-react
* https://www.digitalocean.com/community/tutorials/how-to-add-login-authentication-to-react-applications

frontend
* https://mherman.org/blog/dockerizing-a-react-app/

fetch
* https://www.digitalocean.com/community/tutorials/how-to-call-web-apis-with-the-useeffect-hook-in-react

memo
* https://blog.logrocket.com/solve-react-useeffect-hook-infinite-loop-patterns/#passing-an-incorrect-dependency

styling example
* https://supertokens.com/blog/building-a-login-screen-with-react-and-bootstrap

pagination
* https://stackoverflow.com/questions/65187893/url-adress-and-pagination-react-js-material-ui
* https://www.freecodecamp.org/news/build-a-custom-pagination-component-in-react/
* https://stackoverflow.com/questions/47307273/how-to-display-large-list-of-data-using-reactjs-as-frontend-and-django-rest-fram
* https://www.digitalocean.com/community/tutorials/how-to-build-a-modern-web-application-to-manage-customer-information-with-django-and-react-on-ubuntu-18-04

Go back to next page
* https://bobbyhadz.com/blog/react-router-go-back-to-previous-page#:~:text=To%20go%20back%20to%20the%20previous%20page%2C%20pass%20%2D1%20as,to%20go%202%20pages%20back.

costum pagination and issue:
* https://stackoverflow.com/questions/72105628/get-next-page-number-instead-of-next-page-link-django-rest-framework
* https://github.com/oscarmlage/django-cruds-adminlte/issues/46

API-react-table
* https://www.saaspegasus.com/guides/modern-javascript-for-django-developers/integrating-django-react/
* https://www.valentinog.com/blog/drf/
* https://blog.logrocket.com/using-react-django-create-app-tutorial/#crud-react-components
* https://betterprogramming.pub/how-to-efficiently-display-data-in-tables-with-react-7e133bad5719

Edit
* https://dev.to/fromwentzitcame/working-with-tables-in-react-how-to-render-and-edit-fetched-data-5fl5
* https://blog.logrocket.com/complete-guide-building-smart-data-table-react/
* https://stackoverflow.com/questions/53519578/forms-as-functional-components-with-react

UseEffect:
* https://stackoverflow.com/questions/55938884/react-hook-useeffect-has-a-missing-dependency-list

ERROR Handling
* https://stackoverflow.com/questions/54163952/async-await-in-fetch-how-to-handle-errors

cors
* https://stackoverflow.com/questions/35760943/how-can-i-enable-cors-on-django-rest-framework

api
* https://levelup.gitconnected.com/implementing-classed-based-viewsets-in-django-rest-framework-fd0224852f50

permission
* https://github.com/encode/django-rest-framework/issues/1067

pagination
* https://stackoverflow.com/questions/45670648/how-to-use-pagination-in-a-non-generic-view-viewset/45670649#45670649

celery
* https://rogs.me/2020/11/how-to-create-a-celery-task-that-fills-out-fields-using-django/

celery-test
* https://www.distributedpython.com/2018/05/01/unit-testing-celery-tasks/

task
* https://reqbin.com/code/python/ighnykth/python-requests-post-example
* https://datagy.io/python-requests-post/

test task:
* https://docs.djangoproject.com/en/4.1/topics/testing/advanced/

celery locking
* http://loose-bits.com/2010/10/distributed-task-locking-in-celery.html

celery beat
* https://testdriven.io/courses/django-celery/docker/
* https://testdriven.io/blog/django-celery-periodic-tasks/
* https://www.nickmccullum.com/celery-django-periodic-tasks/#periodic-tasks

managing pwd and filter repo:
* https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository

remove all images non used:
```bash
docker rmi -f $(docker images -f "dangling=true" -q)
```

remove all stopped containers:
```bash
docker rm $(docker ps -a -q)
```

execute django shell:
```bash
docker-compose exec app python manage.py shell
```

then:
```python
from scheduler.tasks import invio_chiamate
invio_chiamate.delay()
```

curl call to add line in db:
```curl
curl -X POST "http://localhost:8000/api/chiamate/chiamate/" -H  "accept: application/json" -H  "Authorization: Token 63eada6fdee0a45f563a483acb692a5fd4fc462c" -H  "Content-Type: application/json" -H  "X-CSRFToken: Xqta8Q8jqlLlwt057xGMenqmFBOGSwRcFEJLYEhx6GRC7HmegaBjTFRicJ0xS3vg" -d "{\"chiamata\":\"<?xml version='1.0' encoding='utf-8'?><Request><Login>login</Login><Password>password</Password></Request>\",\"status\":\"sent request\",\"server\":\"https://httpbin.org/anything\",\"risposta_server_terzo\":\"\"}"
```

