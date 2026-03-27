pipeline {
    agent any

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    environment {
        PROJECT_NAME = 'auto_test_framework'
        CONTAINER_NAME = "pythontest-${PROJECT_NAME}"
        IMAGE_NAME = "pythontest-${PROJECT_NAME}"
        IMAGE_TAG = 'V1.0'
        REPORTS_VOLUME = "test_reports_${PROJECT_NAME}"
        JENKINS_VOLUME = 'jenkins_home'
    }

    stages {
            stage('pull') {
                steps {
                    git credentialsId: '112ff5dee-66f5-4fcc-8f99-563f88813d2c', url: 'git@github.com:dayuuyad/auto_test_framework.git'
                }
            }
            stage('docker build') {
                steps {
                    sh '''
                        if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
                            docker stop ${CONTAINER_NAME}
                            docker rm ${CONTAINER_NAME}
                            echo "容器 ${CONTAINER_NAME} 已删除"
                        else
                            echo "容器 ${CONTAINER_NAME} 不存在"
                        fi

                        if docker images --format '{{.Repository}}:{{.Tag}}' | grep -q "^${IMAGE_NAME}:${IMAGE_TAG}$"; then
                            docker rmi ${IMAGE_NAME}:${IMAGE_TAG}
                            echo "镜像 ${IMAGE_NAME}:${IMAGE_TAG} 已删除"
                        else
                            echo "镜像 ${IMAGE_NAME}:${IMAGE_TAG} 不存在"
                        fi
                        docker build -f docker/Dockerfile -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    '''
                }
            }
            stage('run tests') {
                steps {
                    sh '''
                        docker volume create ${REPORTS_VOLUME} || true
                        
                        docker run --rm \
                            --name ${CONTAINER_NAME} \
                            -v ${REPORTS_VOLUME}:/appnew/reports/allure-results \
                            ${IMAGE_NAME}:${IMAGE_TAG}
                    '''
                }
            }
            stage('generate allure report') {
                steps {
                    sh '''
                        docker run --rm \
                            -v ${REPORTS_VOLUME}:/data \
                            -v ${JENKINS_VOLUME}:/jenkins_home \
                            alpine \
                            sh -c "mkdir -p /jenkins_home/reports/${PROJECT_NAME}/allure-results && cp -r /data/* /jenkins_home/reports/${PROJECT_NAME}/allure-results/"
                    '''
                    script {
                        allure includeProperties: false, jdk: '', results: [[path: "/var/jenkins_home/reports/${PROJECT_NAME}/allure-results"]]
                    }
                }
            }
    }
    post {
        always {
            script {
                def reportUrl = "${BUILD_URL}Allure_20Report/"
                emailext (
                    subject: "$PROJECT_NAME - Build # $BUILD_NUMBER - $BUILD_STATUS!",
                    body: """
$PROJECT_NAME - Build # $BUILD_NUMBER - $BUILD_STATUS:

测试报告地址: ${reportUrl}

Check console output at $BUILD_URL to view the results.
                    """,
                    to: '904977900@qq.com'
                )
            }
        }
        cleanup {
            cleanWs()
        }
    }
}