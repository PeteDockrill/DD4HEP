# CMake generated Testfile for 
# Source directory: /scratch/rg18646/DD4HEP/lcgeo/lcgeoTests
# Build directory: /scratch/rg18646/DD4HEP/lcgeo/build/lcgeoTests
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(t_test_ILD_l5_v02 "/scratch/rg18646/DD4HEP/lcgeo/bin/run_test_lcgeo.sh" "ddsim" "--compactFile=/scratch/rg18646/DD4HEP/lcgeo/lcgeoTests/../ILD/compact/ILD_l5_v02/ILD_l5_v02.xml" "--runType=batch" "-G" "-N=1" "--outputFile=testILD_l5_v02.slcio")
set_tests_properties(t_test_ILD_l5_v02 PROPERTIES  FAIL_REGULAR_EXPRESSION "Exception;EXCEPTION;ERROR;Error")
add_test(t_test_ILD_s5_v02 "/scratch/rg18646/DD4HEP/lcgeo/bin/run_test_lcgeo.sh" "ddsim" "--compactFile=/scratch/rg18646/DD4HEP/lcgeo/lcgeoTests/../ILD/compact/ILD_s5_v02/ILD_s5_v02.xml" "--runType=batch" "-G" "-N=1" "--outputFile=testILD_s5_v02.slcio")
set_tests_properties(t_test_ILD_s5_v02 PROPERTIES  FAIL_REGULAR_EXPRESSION "Exception;EXCEPTION;ERROR;Error")
add_test(t_test_SiD_o2_v02 "/scratch/rg18646/DD4HEP/lcgeo/bin/run_test_lcgeo.sh" "ddsim" "--compactFile=/scratch/rg18646/DD4HEP/lcgeo/lcgeoTests/../SiD/compact/SiD_o2_v02/SiD_o2_v02.xml" "--runType=batch" "-G" "-N=1" "--outputFile=testSiD_o2_v02.slcio")
set_tests_properties(t_test_SiD_o2_v02 PROPERTIES  FAIL_REGULAR_EXPRESSION "Exception;EXCEPTION;ERROR;Error")
add_test(t_test_SiD_o2_v03 "/scratch/rg18646/DD4HEP/lcgeo/bin/run_test_lcgeo.sh" "ddsim" "--compactFile=/scratch/rg18646/DD4HEP/lcgeo/lcgeoTests/../SiD/compact/SiD_o2_v03/SiD_o2_v03.xml" "--runType=batch" "-G" "-N=1" "--outputFile=testSiD_o2_v03.slcio")
set_tests_properties(t_test_SiD_o2_v03 PROPERTIES  FAIL_REGULAR_EXPRESSION "Exception;EXCEPTION;ERROR;Error")
add_test(t_test_CLIC_o1_v01 "/scratch/rg18646/DD4HEP/lcgeo/bin/run_test_lcgeo.sh" "ddsim" "--compactFile=/scratch/rg18646/DD4HEP/lcgeo/lcgeoTests/../CLIC/compact/CLIC_o1_v01/CLIC_o1_v01.xml" "--runType=batch" "-G" "-N=1" "--outputFile=testCLIC.slcio")
set_tests_properties(t_test_CLIC_o1_v01 PROPERTIES  FAIL_REGULAR_EXPRESSION "Exception;EXCEPTION;ERROR;Error")
add_test(t_test_CLIC_o2_v04 "/scratch/rg18646/DD4HEP/lcgeo/bin/run_test_lcgeo.sh" "ddsim" "--compactFile=/scratch/rg18646/DD4HEP/lcgeo/lcgeoTests/../CLIC/compact/CLIC_o2_v04/CLIC_o2_v04.xml" "--runType=batch" "-G" "-N=1" "--outputFile=testCLIC_o2_v04.slcio")
set_tests_properties(t_test_CLIC_o2_v04 PROPERTIES  FAIL_REGULAR_EXPRESSION "Exception;EXCEPTION;ERROR;Error")
add_test(t_test_CLIC_o3_v14 "/scratch/rg18646/DD4HEP/lcgeo/bin/run_test_lcgeo.sh" "ddsim" "--compactFile=/scratch/rg18646/DD4HEP/lcgeo/lcgeoTests/../CLIC/compact/CLIC_o3_v14/CLIC_o3_v14.xml" "--runType=batch" "-G" "-N=1" "--outputFile=testCLIC_o3_v14.slcio")
set_tests_properties(t_test_CLIC_o3_v14 PROPERTIES  FAIL_REGULAR_EXPRESSION "Exception;EXCEPTION;ERROR;Error")
add_test(t_test_FCCee_o1_v04 "/scratch/rg18646/DD4HEP/lcgeo/bin/run_test_lcgeo.sh" "ddsim" "--compactFile=/scratch/rg18646/DD4HEP/lcgeo/lcgeoTests/../FCCee/compact/FCCee_o1_v04/FCCee_o1_v04.xml" "--runType=batch" "-G" "-N=1" "--outputFile=testFCCee_o1_v04.slcio")
set_tests_properties(t_test_FCCee_o1_v04 PROPERTIES  FAIL_REGULAR_EXPRESSION "Exception;EXCEPTION;ERROR;Error")
add_test(t_test_FCCee_dev "/scratch/rg18646/DD4HEP/lcgeo/bin/run_test_lcgeo.sh" "ddsim" "--compactFile=/scratch/rg18646/DD4HEP/lcgeo/lcgeoTests/../FCCee/compact/FCCee_dev/FCCee_dev.xml" "--runType=batch" "-G" "-N=1" "--outputFile=testFCCee_dev.slcio")
set_tests_properties(t_test_FCCee_dev PROPERTIES  FAIL_REGULAR_EXPRESSION "Exception;EXCEPTION;ERROR;Error")
add_test(t_test_steeringFile "/scratch/rg18646/DD4HEP/lcgeo/bin/run_test_lcgeo.sh" "ddsim" "--steeringFile=/scratch/rg18646/DD4HEP/lcgeo/lcgeoTests/../example/steeringFile.py" "--compactFile=/scratch/rg18646/DD4HEP/lcgeo/lcgeoTests/../CLIC/compact/CLIC_o2_v04/CLIC_o2_v04.xml" "--runType=batch" "-G" "-N=1" "--outputFile=testCLIC_o2_v04.slcio")
set_tests_properties(t_test_steeringFile PROPERTIES  FAIL_REGULAR_EXPRESSION "Exception;EXCEPTION;ERROR;Error")
add_test(t_SensThickness_Clic_o2_v4 "/scratch/rg18646/DD4HEP/lcgeo/bin/run_test_lcgeo.sh" "/scratch/rg18646/DD4HEP/lcgeo/bin/TestSensThickness" "/scratch/rg18646/DD4HEP/lcgeo/lcgeoTests/../CLIC/compact/CLIC_o2_v04/CLIC_o2_v04.xml" "300" "50")
add_test(t_SensThickness_CLIC_o3_v14 "/scratch/rg18646/DD4HEP/lcgeo/bin/run_test_lcgeo.sh" "/scratch/rg18646/DD4HEP/lcgeo/bin/TestSensThickness" "/scratch/rg18646/DD4HEP/lcgeo/lcgeoTests/../CLIC/compact/CLIC_o3_v14/CLIC_o3_v14.xml" "100" "50")
