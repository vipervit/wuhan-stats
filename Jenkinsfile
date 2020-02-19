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
           sh 'python3 -m twine upload -u vipervit dist/wuhan_stats*'
           sh 'pyinstaller --onefile --windowed wuhanstats.py'
        }
       }

    }

}
