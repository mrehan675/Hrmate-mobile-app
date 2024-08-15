// Copyright (c) 2024, rehan and contributors
// For license information, please see license.txt

frappe.ui.form.on('Mobile App Setting', {
    token: function(frm) {
        
        frm.set_value("custom_token", frm.doc.token);
        
       
    }
});

