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
           sh 'python3 -m twine upload dist/* -u vipervit'
        }
       }

       stage('DEPLOY') {
        steps {
            sh 'pip install --upgrade viperdriver'
            sh 'pip install --upgrade wuhan-stats'
            sh 'kill -9 `ps -ef | grep wuhan-stats | awk '{print \$2}'` >/dev/null 2>&1'
        }
       }

    }

}
