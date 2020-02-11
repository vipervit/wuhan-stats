pipeline {

  agent any

    stages {

       stage('BUILD') {
        steps {
            sh 'source $python_prog/dev/bin/activate'
            sh 'rm -r -f dist'
            sh 'python3 setup.py sdist'
        }
       }

       stage('UPLOAD - TESTPYPI') {
        steps {
           sh 'twine upload -u vipervit --repository-url https://test.pypi.org/legacy/ dist/*'
        }
       }

       stage('DEPLOY - TESTPYPI') {
        steps {
            sh 'source $python_prog/test/bin/activate'
            sh 'pip install --index-url https://test.pypi.org/simple/ wuhan-stats'
        }
       }

    }

}
