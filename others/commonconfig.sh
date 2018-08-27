alias mvnci="mvn clean install -DskipTests"

function gitpacp {
	git pull origin master;
	git add .;
	git commit -m "yu-T440";
	git push origin master;
}

function gitacp {
	git add .;
	git commit -m "yu-T440";
	git push origin master;
}

function gitac {
	git add .;
	git commit -m "yu-T440";
}

