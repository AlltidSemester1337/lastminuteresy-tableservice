<h1>Lastminuteresy table-service</h1>

<p>
Service for managing "owned" bookings as well as request booking to be made.
</p>

<h2>Deploy process</h2>
<p>TBA</p>
<!-- <p>prerequisties: docker image (see above) and aws account / credentials configured</p>
<ul>
<li>confirm container service ready: <br>
aws lightsail get-container-services  \
    --region eu-west-3                \
    --service-name lastminutetableresy-web \
    --query "containerServices[].state"</li>
<li>push image:<br>
aws lightsail push-container-image    \
    --region eu-west-3                \
    --service-name lastminutetableresy-web \
    --label latest                    \
    --image ktor-docker-image:latest</li>
<li>(optional) get new image(?) name<br>
aws lightsail get-container-images    \
    --region eu-west-3                \
    --service-name lastminutetableresy-web</li>
<li>Update deploy.json file with image name</li>
<li><strong>create deployment for new image</strong><br>
aws lightsail create-container-service-deployment \
    --region eu-west-3                            \
    --cli-input-json "deploy.json_full_file_path"</li>
<li>get deployment state (takes up to 3 min):<br>
aws lightsail get-container-services      \
    --region eu-west-3                    \
    --query "containerServices[].nextDeployment.state"
<br>alternatively<br>
aws lightsail get-container-services      \
    --region eu-west-3                    \
    --query "containerServices[].currentDeployment.state"</li>
<li>get deployed container url<br>
aws lightsail get-container-services        \
    --region eu-west-3                      \
    --query "containerServices[].url"</li>
<li>???</li>
<li>Profit</li>

</ul>
-->