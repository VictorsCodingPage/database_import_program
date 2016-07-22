properties {
  $initMessage = 'Initializing!'
  $testMessage = 'Executed Test!'
  $compileMessage = 'Executed Compile!'
  $cleanMessage = 'Executed Clean!'
  $releaseDirectory = '.\release'
  $tearDownMessage = 'Tearing Down!'
}

task default -Depends Test

Task Test -Depends Clean{
   try{
        exec{py -2 -m unittest discover}
   }
   catch{
        throw
   }
   finally{
        Invoke-Expression "deactivate"
   }
}

Task Clean -Depends Init {
   $cleanMessage = 'Executed Clean!'
   Remove-Item "$releaseDirectory\*"
}

Task Init {
   exec{& "./env/scripts/activate.ps1"}
   Invoke-Expression "pip install psycopg2"
}



