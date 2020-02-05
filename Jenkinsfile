pipeline {

  agent any

    stages {

      stage('BUILD') {
        steps {
          sh 'rm -r -f dist'
          sh 'python3 setup.py sdist'
       }
      }

      stage('UPLOAD') {
        steps {
          sh 'python3 -m twine upload dist/* -u wuhan'
        }
       }

      stage('DEPLOY') {
        steps {
          sh 'source $PROG/python/prod/bin/activate ; pip install --upgrade wuhan'
        }
       }

    }
}
