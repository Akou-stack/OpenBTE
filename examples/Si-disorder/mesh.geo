Point(0) = {10.0,5.8425,0,1.0};
Point(1) = {9.0199,5.8425,0,1.0};
Point(2) = {9.0199,9.7155,0,1.0};
Point(3) = {10.0,9.7155,0,1.0};
Point(4) = {10.0,10.0,0,1.0};
Point(5) = {-0.1647,10.0,0,1.0};
Point(6) = {-0.1647,8.7486,0,1.0};
Point(7) = {-4.0377,8.7486,0,1.0};
Point(8) = {-4.0377,10.0,0,1.0};
Point(9) = {-10.0,10.0,0,1.0};
Point(10) = {-10.0,9.7155,0,1.0};
Point(11) = {-7.1071,9.7155,0,1.0};
Point(12) = {-7.1071,5.8425,0,1.0};
Point(13) = {-10.0,5.8425,0,1.0};
Point(14) = {-10.0,-10.0,0,1.0};
Point(15) = {-4.0377,-10.0,0,1.0};
Point(16) = {-4.0377,-7.3784,0,1.0};
Point(17) = {-0.1647,-7.3784,0,1.0};
Point(18) = {-0.1647,-10.0,0,1.0};
Point(19) = {10.0,-10.0,0,1.0};
Line(1) = {0,1};
Line(2) = {1,2};
Line(3) = {2,3};
Line(4) = {3,4};
Line(5) = {4,5};
Line(6) = {5,6};
Line(7) = {6,7};
Line(8) = {7,8};
Line(9) = {8,9};
Line(10) = {9,10};
Line(11) = {10,11};
Line(12) = {11,12};
Line(13) = {12,13};
Line(14) = {13,14};
Line(15) = {14,15};
Line(16) = {15,16};
Line(17) = {16,17};
Line(18) = {17,18};
Line(19) = {18,19};
Line(20) = {19,0};
Line Loop(0) = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20};
Point(20) = {-6.5012,0.4839,0,1.0};
Point(21) = {-6.5012,4.3569,0,1.0};
Point(22) = {-2.6282,4.3569,0,1.0};
Point(23) = {-2.6282,0.4839,0,1.0};
Line(21) = {20,21};
Line(22) = {21,22};
Line(23) = {22,23};
Line(24) = {23,20};
Line Loop(1) = {21,22,23,24};
Point(24) = {4.0955,-7.8174,0,1.0};
Point(25) = {4.0955,-3.9444,0,1.0};
Point(26) = {7.9685,-3.9444,0,1.0};
Point(27) = {7.9685,-7.8174,0,1.0};
Line(25) = {24,25};
Line(26) = {25,26};
Line(27) = {26,27};
Line(28) = {27,24};
Line Loop(2) = {25,26,27,28};
Plane Surface(0) = {0,1,2};
Physical Surface('Bulk') = {0};
Physical Line('Periodic_1') = {10,14};
Physical Line('Periodic_2') = {4,20};
Physical Line('Periodic_3') = {5,9};
Physical Line('Periodic_4') = {15,19};
Physical Line('Boundary') = {8,7,6,3,2,1,11,13,12,22,21,24,23,26,25,28,27,17,16,18};
Periodic Line{10}={-4};
Periodic Line{14}={-20};
Periodic Line{15}={-9};
Periodic Line{19}={-5};