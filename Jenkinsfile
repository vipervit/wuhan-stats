pipeline {

  agent any

    stages {

       stage('BUILD') {
        steps {
            sh 'rm -r -f dist'
            sh 'python3 setup.py sdist'
        }
       }

       stage('UPLOAD - TESTPYPI') {
        steps {
           sh 'python3 -m twine upload -u wuhan-stats --repository-url https://test.pypi.org/legacy/ dist/*'
        }
       }

       stage('DEPLOY - TESTPYPI') {
        steps {
            sh 'pip install viperdriver'
            sh 'source $PROG/python/dev/bin/activate ; pip install --index-url https://test.pypi.org/simple/ wuhan-stats'
        }
       }

    }

}
