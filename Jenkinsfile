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
           sh 'twine upload --repository-url https://test.pypi.org/legacy/ dist/*'
        }
       }

       stage('DEPLOY') {
        steps {
            sh 'pip install --upgrade --index-url https://test.pypi.org/simple/ wuhan-stats'
        }
       }

    }

}
