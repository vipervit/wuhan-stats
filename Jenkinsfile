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
           sh 'pip install --upgrade --index-url https://test.pypi.org/simple/ wuhan_stats -r requirements.txt'
        }
       }

       stage('DEPLOY') {
        steps {
            sh 'pip install --upgrade wuhan_stats'
        }
       }

    }

}
