package com.example.robotcatmobile;

import android.os.Build;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import androidx.viewpager2.widget.ViewPager2;

import android.view.ViewTreeObserver;
import com.example.robotcatmobile.home_parts.Frag_SetObs;
import com.example.robotcatmobile.home_parts.Frag_ptz;
import com.example.robotcatmobile.home_parts.Frag_timer;
import com.example.robotcatmobile.home_parts.GridRecycler;
import com.example.robotcatmobile.home_parts.VPAdapter;
import com.google.android.material.tabs.TabLayout;
import com.google.android.material.tabs.TabLayoutMediator;


/**
 * A simple {@link Fragment} subclass.
 * create an instance of this fragment.
 */
@RequiresApi(api = Build.VERSION_CODES.N)
public class HomeFrag extends Fragment {
    public HomeFrag() {
        // Required empty public constructor
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_home, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        // get the grid layout
        RecyclerView mGridLayout = view.findViewById(R.id.grid);
        GridRecycler gridRecycler = new GridRecycler();
        mGridLayout.setAdapter(gridRecycler);
        // span count in this case is the number of columns
        mGridLayout.setLayoutManager(new GridLayoutManager(getContext(),GridRecycler.COLUMNS));
        // for task 1
        mGridLayout.getViewTreeObserver().addOnGlobalLayoutListener(new ViewTreeObserver.OnGlobalLayoutListener(){
            @Override
            public void onGlobalLayout() {
                // the layout is completed
                gridRecycler.placeRobot(0, 19);
                // and set the grid!
                for (int num = 0; num < gridRecycler.arrOfGrids.length; ++num) {
                    gridRecycler.arrOfGrids[num].setObstacle(false);
                }
            mGridLayout.getViewTreeObserver().removeOnGlobalLayoutListener( this);
        }
        });

        VPAdapter myVP = new VPAdapter(this);
        TabLayout mTabLayouts = view.findViewById(R.id.home_tab_layouts);
        ViewPager2 mViewPager = view.findViewById(R.id.home_viewpager);

        mViewPager.setAdapter(myVP);
        myVP.addFrag(new Frag_ptz());
        myVP.addFrag(new Frag_timer(gridRecycler));
        myVP.addFrag(new Frag_SetObs());
        myVP.createFragment(0);
        new TabLayoutMediator(mTabLayouts, mViewPager, ((tab, position) -> {
            // LMAO, just hardcode!
            if (position == 0) {
                tab.setText("PTZ");
            }
            else if (position == 1) {
                tab.setText("TIMER");
            }
            else {
                tab.setText("SET");
            }
        })).attach();
    }
}
