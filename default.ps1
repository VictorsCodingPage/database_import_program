properties {
  $initMessage = 'Initializing!'
  $testMessage = 'Executed Test!'
  $compileMessage = 'Executed Compile!'
  $cleanMessage = 'Executed Clean!'
  $releaseDirectory = '.\release'
  $tearDownMessage = 'Tearing Down!'
}

task default -Depends Test

Task TearDown -Depends Compile{
    Remove-Item "$temp\*"
}

Task Compile -Depends Test{
    Expand-Archive -Path static_html.html -DestinationPath temp
}

Task Test -Depends Clean{
   try{
        exec{python -m unittest discover}
   }
   catch{
        throw
   }
   finally{
        Invoke-Expression "deactivate"
   }
}

Task Clean -Depends Init {
   $cleanMessage
   Remove-Item "$releaseDirectory\*"
}

Task Init {
   exec{& "virtualenv env"}
   exec{& "./env/scripts/activate.ps1"}
   Invoke-Expression "pip install psycopg2"
   Invoke-Expression "pip install flask"
   Invoke-Expression "pip install flask_restful"
   Invoke-Expression "pip install bs4"
}



