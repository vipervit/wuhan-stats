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
           sh 'python3 -m twine upload -u vipervit dist/*'
        }
       }

       stage('DEPLOY') {
        steps {
            sh 'pip install --upgrade wuhan_stats -r requirements.txt'
        }
       }

    }

}
