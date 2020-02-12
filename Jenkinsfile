pipeline {

  agent any

    stages {

       stage('BUILD') {
        steps {
            sh '. $$python_prog/dev/bin/activate'
            sh 'rm -r -f dist'
            sh 'python3 setup.py sdist'
        }
       }

       stage('UPLOAD - TESTPYPI') {
        steps {
           sh 'python3 -m twine upload -u vipervit --repository-url https://test.pypi.org/legacy/ dist/*'
        }
       }

       stage('DEPLOY - STAGING') {
        steps {
            sh '. $$python_prog/test/bin/activate'
            sh 'pip install --index-url https://test.pypi.org/simple/ wuhan-stats'
        }
       }

       stage('RESTART APPLICATION') {
       steps {
            sh '. ~/sh/wuhan/wuhan-stop.sh'
            sh '. ~/sh/wuhan/wuhan-start.sh'
        }
       }

    }

}
