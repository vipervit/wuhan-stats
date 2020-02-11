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
           sh 'twine upload -u vipervit --repository-url https://test.pypi.org/legacy/ dist/*'
        }
       }

       stage('DEPLOY') {
        steps {
            sh 'source $PROG/python/test/bin/activate'
            sh 'pip install --index-url https://test.pypi.org/simple/ wuhan-stats'
        }
       }

    }

}
