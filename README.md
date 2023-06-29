# Attendence-System-by-Face-Recognition
<!DOCTYPE html>
<html>
<head>
</head>
<body>
    <ul>
      <li>Python project implementing attendance system with face recognition</li>
      <li>Uses computer vision and deep learning for accurate identification</li>
      <li>Eliminates manual attendance records and reduces errors/fraud</li>
      <li>Generates reports and analytics on attendance patterns</li>
      <li>New faces can be added at any time</li>
      <li>Provides information on classes attended by students and number of students attended on specific dates</li>
      <li>Comprehensive attendance management solution for organizations with high accuracy and reliability.</li>
    </ul>
	<h2>Installation</h2>
	<ol>
		<li>Clone the repository to your local machine using the following command:</li>
		<pre><code>git clone https://github.com/curious-99/Attendence-System-by-Face-Recognition.git</code></pre>
		<li>Install the required libraries using pip:</li>
		<pre><code>pip install -r requirements.txt</code></pre>
		<li>Download the pre-trained face recognition model from <a href="https://github.com/SinghAnkit1010/Attendence-System-by-Face-Recognition">here</a>.</li>
		<li>Copy the downloaded model to the <code>models</code> directory.</li>
	</ol>
	<h2>Usage</h2>
	<ol>
		<li>Add images of the persons whose attendance is to be marked in the <code>images</code> directory.</li>
		<li>Run the following command to register the images:</li>
		<pre><code>python register.py</code></pre>
		<li>Run the following command to start the attendance system:</li>
		<pre><code>python attendance.py</code></pre>
		<li>The attendance records will be stored in the <code>attendance.csv</code> file.</li>
	</ol>
	<h2>Credits</h2>
	<p>This project uses the following libraries:</p>
	<ul>
		<li>face_recognition</li>
		<li>opencv-python</li>
		<li>numpy</li>
	</ul>
	<h2>License</h2>
	<p>This project is licensed under the <a href="https://opensource.org/licenses/MIT">MIT License</a>.</p>
</body>


