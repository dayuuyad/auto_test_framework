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
                    checkout scm  // 使用 Jenkins 任务配置的分支
                    //git credentialsId: '112ff5dee-66f5-4fcc-8f99-563f88813d2c', url: 'git@github.com:dayuuyad/auto_test_framework.git'
                    //git branch: 'main', credentialsId: '112ff5dee-66f5-4fcc-8f99-563f88813d2c', url: 'git@github.com:dayuuyad/auto_test_framework.git'
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
                            -v ${REPORTS_VOLUME}:/appnew/reports \
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
                            sh -c "mkdir -p /jenkins_home/reports/${PROJECT_NAME}/allure-results && cp -r /data/allure-results/* /jenkins_home/reports/${PROJECT_NAME}/allure-results/"
                        
                        # 删除可能存在的旧链接
                        rm -f ${WORKSPACE}/allure-results
                        
                        # 创建符号链接
                        ln -sf /var/jenkins_home/reports/${PROJECT_NAME}/allure-results ${WORKSPACE}/allure-results                            
                    '''
                    script {
                        def resultsPath = "/var/jenkins_home/reports/${env.PROJECT_NAME}/allure-results"
                        echo "Allure 结果路径: ${resultsPath}"
                    // 生成并发布 Allure 报告
                    allure([
                        commandline: 'allure',
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS'
                    ])
                        
                    }
                }
            }
    }
    post {
        always {
            script {
                try {
                    def buildStatus = currentBuild.currentResult ?: 'UNKNOWN'
                    def reportUrl = "${env.BUILD_URL}allure/"
                    emailext (
                        subject: "${env.PROJECT_NAME} - Build # ${env.BUILD_NUMBER} - ${buildStatus}!",
                        body: """
${env.PROJECT_NAME} - Build # ${env.BUILD_NUMBER} - ${buildStatus}:

测试报告地址: ${reportUrl}

Check console output at ${env.BUILD_URL} to view the results.
                        """,
                        to: '904977900@qq.com'
                    )
                    echo "邮件发送成功"
                } catch (Exception e) {
                    echo "邮件发送失败: ${e.getMessage()}"
                }
            }
        }
        cleanup {
            cleanWs()
        }
    }
}