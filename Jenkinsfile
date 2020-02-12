pipeline {

  agent any

    stages {

      stage('GET SHELL ENV') {
       steps{
            sh 'source /etc/profile'
       }
      }

       stage('BUILD') {
        steps {
            sh 'pdev'
            sh 'rm -r -f dist'
            sh 'python3 setup.py sdist'
        }
       }

       stage('UPLOAD - TESTPYPI') {
        steps {
           sh 'python3 -m twine upload -u vipervit --repository-url https://test.pypi.org/legacy/ dist/*'
        }
       }

       stage('DEPLOY - TESTPYPI') {
        steps {
            sh 'ptest'
            sh 'pip install --index-url https://test.pypi.org/simple/ wuhan-stats'
        }
       }

       stage('RESTART') {
       steps {
            sh 'wuhan-stop'
            sh 'wuhan-start'
        }
       }

    }

}
