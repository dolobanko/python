#!/usr/bin/env python

import os
import boto3

versionsLimit = 15

eb_client = boto3.client('elasticbeanstalk', 
	region_name=os.environ['AWS_REGION'],
	aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
	aws_secret_access_key=os.environ['AWS_SECRET_KEY']
	)

def cleanup():
	applicationList = eb_client.describe_applications()['Applications']
	for application in applicationList:
		applicationName = application['ApplicationName']
		print "Cleaning application: %s" % applicationName
		applicationVerions = eb_client.describe_application_versions(ApplicationName=applicationName)['ApplicationVersions']
		print ' * Application versions: %s' % len(applicationVerions)

		sortedList = sorted(applicationVerions, key=lambda v: v['DateCreated'], reverse=True)
		sortedListCount = len(sortedList)
		listDiff = sortedListCount - versionsLimit
		if (listDiff > 0):
			versionToDelete = [version['VersionLabel'] for version in sortedList[versionsLimit:sortedListCount]]
			print ' *** Versions to remove %s: %s' % (len(versionToDelete), versionToDelete)

			environments = eb_client.describe_environments(ApplicationName=applicationName)['Environments']
			deployedVersions = [environment['VersionLabel'] for environment in environments]
			print ' *** Deployed Versions: %s' % (deployedVersions)

			finalVersionsToDelete = set(versionToDelete).difference(set(deployedVersions))
			print ' *** FInal Versions to delete (%s,  excluding the ones that are deployed): %s' % (len(finalVersionsToDelete), finalVersionsToDelete)

			for version in finalVersionsToDelete:
				  print ' **** Deleting Version : %s ' % version
				  eb_client.delete_application_version(ApplicationName=applicationName, VersionLabel=version, DeleteSourceBundle=True)
		    
			print   ' *** Application Versions deleted: %s, bye' % len(finalVersionsToDelete)


		else:
			print ' *** Application Versions number %s is lower than the limit %s' % (sortedListCount, versionsLimit)

if __name__ == "__main__" :
	cleanup()
