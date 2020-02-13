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
           sh 'python3 -m twine upload -u vipervit --repository-url https://test.pypi.org/legacy/ dist/*'
        }
       }

       stage('DEPLOY - STAGE') {
        steps {
            sh 'pip install --upgrade --index-url https://test.pypi.org/simple/ wuhan_stats'
        }
       }

    }

}
