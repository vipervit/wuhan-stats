pipeline {

  agent any

    stages {

       stage('BUILD') {
        steps {
            sh 'rm -r -f dist'
            sh 'python3 setup.py sdist'
        }
       }

       stage('UPLOAD - TEST') {
        steps {
           sh 'python3 -m twine upload -u vipervit --index-url https://test.pypi.org/simple/ dist/*'
        }
       }

       stage('DEPLOY - TEST') {
        steps {
            sh 'pip install --upgrade wuhan_stats --index-url https://test.pypi.org/simple/ -r requirements.txt'
        }
       }

    }

}
