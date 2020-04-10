def get_org_approval_mail(org_id, org_name):
    org_approval_mail = {
        "subject": f"""Organization Approval: organization ({org_id, org_name})""",
        "body": """\
<html>
    <head></head>
    <body>
        <div>
            <p>Hello,</p>
            <p>The following organization has been submitted for approval. Please review,</p>
            <p>Organization id: <strong>{org_id}</strong><br/>
            Organization name: <strong>{org_name}</strong><br/></p>
        </div>
        <br/>

        <i><p>Steps for approval:</p>
        <ul>
            <li>Go to approval channel</li>
            <li><strong>/list-orgs-for-approval</strong> command to get list of services</li>
            <li>To review the particular service click on <strong>review</strong>, it will open pop up window</li>
            <li>Select appropriate options (Approved, Rejected, Change requested) and give comment.</li>
            <li>Click on <strong>submit</strong> to review the service.</li>
        </ul></i>

        <br/>
        <p>Regards,<br/>SingularityNET Publisher Portal Team</p>

    </body>
</html> \
"""
    }
    return org_approval_mail
